import * as cdk from 'aws-cdk-lib/core';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as apigwv2 from 'aws-cdk-lib/aws-apigatewayv2';
import * as apigwv2Integrations from 'aws-cdk-lib/aws-apigatewayv2-integrations';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as rds from 'aws-cdk-lib/aws-rds';
import { Construct } from 'constructs';

interface ComputeStackProps extends cdk.StackProps {
  vpc: ec2.Vpc;
  lambdaSecurityGroup: ec2.SecurityGroup;
  dbCluster: rds.DatabaseCluster;
  rawDataBucket: s3.Bucket;
  processedDataBucket: s3.Bucket;
  modelArtifactsBucket: s3.Bucket;
}

export class ComputeStack extends cdk.Stack {
  public readonly ingestionFn: lambda.Function;
  public readonly featureEngineeringFn: lambda.Function;
  public readonly inferenceFn: lambda.Function;
  public readonly resultsFn: lambda.Function;

  constructor(scope: Construct, id: string, props: ComputeStackProps) {
    super(scope, id, props);

    const backendPath = '../../../backend';

    // Shared environment variables for all Lambdas
    const sharedEnv = {
      DB_SECRET_ARN: props.dbCluster.secret!.secretArn,
      RAW_DATA_BUCKET: props.rawDataBucket.bucketName,
      PROCESSED_DATA_BUCKET: props.processedDataBucket.bucketName,
      MODEL_ARTIFACTS_BUCKET: props.modelArtifactsBucket.bucketName,
    };

    // Shared Lambda config
    const sharedLambdaProps = {
      runtime: lambda.Runtime.PYTHON_3_11,
      timeout: cdk.Duration.minutes(5),
      memorySize: 512,
      vpc: props.vpc,
      vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS },
      securityGroups: [props.lambdaSecurityGroup],
      environment: sharedEnv,
    };

    // --- Lambda Functions ---

    this.ingestionFn = new lambda.Function(this, 'IngestionFunction', {
      ...sharedLambdaProps,
      functionName: 'equine-ingestion',
      description: 'Pulls daily race entries and PP data from Equibase',
      code: lambda.Code.fromAsset(`${backendPath}/lambdas/ingestion`),
      handler: 'handler.handler',
    });

    this.featureEngineeringFn = new lambda.Function(this, 'FeatureEngineeringFunction', {
      ...sharedLambdaProps,
      functionName: 'equine-feature-engineering',
      description: 'Transforms raw PP data into model features',
      code: lambda.Code.fromAsset(`${backendPath}/lambdas/feature-engineering`),
      handler: 'handler.handler',
    });

    this.inferenceFn = new lambda.Function(this, 'InferenceFunction', {
      ...sharedLambdaProps,
      functionName: 'equine-inference',
      description: 'Loads model artifact and runs predictions on upcoming races',
      memorySize: 1024,
      code: lambda.Code.fromAsset(`${backendPath}/lambdas/inference`),
      handler: 'handler.handler',
    });

    this.resultsFn = new lambda.Function(this, 'ResultsFunction', {
      ...sharedLambdaProps,
      functionName: 'equine-results',
      description: 'Ingests race results for model evaluation',
      code: lambda.Code.fromAsset(`${backendPath}/lambdas/results`),
      handler: 'handler.handler',
    });

    // --- IAM Permissions ---

    // All Lambdas can read DB credentials from Secrets Manager
    props.dbCluster.secret!.grantRead(this.ingestionFn);
    props.dbCluster.secret!.grantRead(this.featureEngineeringFn);
    props.dbCluster.secret!.grantRead(this.inferenceFn);
    props.dbCluster.secret!.grantRead(this.resultsFn);

    // Ingestion writes raw data
    props.rawDataBucket.grantReadWrite(this.ingestionFn);

    // Feature engineering reads raw, writes processed
    props.rawDataBucket.grantRead(this.featureEngineeringFn);
    props.processedDataBucket.grantReadWrite(this.featureEngineeringFn);

    // Inference reads model artifacts and processed data
    props.modelArtifactsBucket.grantRead(this.inferenceFn);
    props.processedDataBucket.grantRead(this.inferenceFn);

    // Results reads raw data (for race IDs) and writes processed (scoring output)
    props.rawDataBucket.grantRead(this.resultsFn);
    props.processedDataBucket.grantReadWrite(this.resultsFn);

    // --- EventBridge Cron Schedule ---

    // 6 AM ET = 11 AM UTC — pull daily entries
    new events.Rule(this, 'IngestionSchedule', {
      ruleName: 'equine-ingestion-daily',
      schedule: events.Schedule.expression('cron(0 11 * * ? *)'),
      targets: [new targets.LambdaFunction(this.ingestionFn)],
    });

    // 7 AM ET = 12 PM UTC — transform raw data into features
    new events.Rule(this, 'FeatureEngineeringSchedule', {
      ruleName: 'equine-feature-engineering-daily',
      schedule: events.Schedule.expression('cron(0 12 * * ? *)'),
      targets: [new targets.LambdaFunction(this.featureEngineeringFn)],
    });

    // 7:30 AM ET = 12:30 PM UTC — run predictions
    new events.Rule(this, 'InferenceSchedule', {
      ruleName: 'equine-inference-daily',
      schedule: events.Schedule.expression('cron(30 12 * * ? *)'),
      targets: [new targets.LambdaFunction(this.inferenceFn)],
    });

    // 11 PM ET = 4 AM UTC next day — ingest results
    new events.Rule(this, 'ResultsSchedule', {
      ruleName: 'equine-results-daily',
      schedule: events.Schedule.expression('cron(0 4 * * ? *)'),
      targets: [new targets.LambdaFunction(this.resultsFn)],
    });

    // --- HTTP API Gateway ---

    const httpApi = new apigwv2.HttpApi(this, 'EquineApi', {
      apiName: 'equine-api',
      description: 'HTTP API for Equine Equalizer race predictions',
      corsPreflight: {
        allowOrigins: ['*'],
        allowMethods: [apigwv2.CorsHttpMethod.GET],
        allowHeaders: ['Content-Type'],
      },
    });

    const inferenceIntegration = new apigwv2Integrations.HttpLambdaIntegration(
      'InferenceIntegration',
      this.inferenceFn,
    );

    httpApi.addRoutes({
      path: '/races/today',
      methods: [apigwv2.HttpMethod.GET],
      integration: inferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/races/{date}',
      methods: [apigwv2.HttpMethod.GET],
      integration: inferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/races/{raceId}/detail',
      methods: [apigwv2.HttpMethod.GET],
      integration: inferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/health',
      methods: [apigwv2.HttpMethod.GET],
      integration: inferenceIntegration,
    });

    new cdk.CfnOutput(this, 'ApiUrl', {
      value: httpApi.apiEndpoint,
      exportName: 'EquineApiUrl',
    });
  }
}
