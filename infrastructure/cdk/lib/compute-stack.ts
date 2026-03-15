import * as path from 'path';
import * as cdk from 'aws-cdk-lib/core';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as apigwv2 from 'aws-cdk-lib/aws-apigatewayv2';
import * as apigwv2Integrations
  from 'aws-cdk-lib/aws-apigatewayv2-integrations';
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

  constructor(
    scope: Construct,
    id: string,
    props: ComputeStackProps
  ) {
    super(scope, id, props);

    const backendPath = path.join(
      __dirname, '../../../backend'
    );
    const projectRoot = path.join(
      __dirname, '../../..'
    );

    // Shared environment variables
    const sharedEnv = {
      DB_SECRET_ARN: props.dbCluster.secret!.secretArn,
      RAW_DATA_BUCKET: props.rawDataBucket.bucketName,
      PROCESSED_DATA_BUCKET:
        props.processedDataBucket.bucketName,
      MODEL_ARTIFACTS_BUCKET:
        props.modelArtifactsBucket.bucketName,
    };

    // Shared Lambda config for container Lambdas
    // No runtime specified — container provides it
    // No layers — packages are in the container
    const sharedProps = {
      timeout: cdk.Duration.minutes(5),
      memorySize: 512,
      vpc: props.vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS
      },
      securityGroups: [props.lambdaSecurityGroup],
      environment: sharedEnv,
    };

    // ─────────────────────────────────────
    // Lambda Functions (Docker container images)
    // CDK automatically:
    // 1. Runs docker build using the Dockerfile
    // 2. Creates an ECR repository
    // 3. Pushes the image to ECR
    // 4. Wires Lambda to use the ECR image
    // ─────────────────────────────────────

    this.ingestionFn = new lambda.DockerImageFunction(
      this,
      'IngestionFunction',
      {
        ...sharedProps,
        functionName: 'equine-ingestion',
        description:
          'Pulls daily race entries and PP data',
        code: lambda.DockerImageCode.fromImageAsset(
          projectRoot,
          {
            file: 'Dockerfile.ingestion',
          }
        ),
      }
    );

    this.featureEngineeringFn =
      new lambda.DockerImageFunction(
        this,
        'FeatureEngineeringFunction',
        {
          ...sharedProps,
          functionName: 'equine-feature-engineering',
          description:
            'Transforms raw PP data into features',
          code: lambda.DockerImageCode.fromImageAsset(
            projectRoot,
            {
              file: 'Dockerfile.feature-engineering',
            }
          ),
        }
      );

    this.inferenceFn = new lambda.DockerImageFunction(
      this,
      'InferenceFunction',
      {
        ...sharedProps,
        functionName: 'equine-inference',
        description:
          'Loads model and runs predictions',
        memorySize: 1024,
        code: lambda.DockerImageCode.fromImageAsset(
          projectRoot,
          {
            file: 'Dockerfile.inference',
          }
        ),
      }
    );

    this.resultsFn = new lambda.DockerImageFunction(
      this,
      'ResultsFunction',
      {
        ...sharedProps,
        functionName: 'equine-results',
        description: 'Ingests race results',
        code: lambda.DockerImageCode.fromImageAsset(
          projectRoot,
          {
            file: 'Dockerfile.results',
          }
        ),
      }
    );

    // ─────────────────────────────────────
    // IAM Permissions (unchanged)
    // ─────────────────────────────────────

    props.dbCluster.secret!.grantRead(
      this.ingestionFn
    );
    props.dbCluster.secret!.grantRead(
      this.featureEngineeringFn
    );
    props.dbCluster.secret!.grantRead(
      this.inferenceFn
    );
    props.dbCluster.secret!.grantRead(
      this.resultsFn
    );

    props.rawDataBucket.grantReadWrite(
      this.ingestionFn
    );
    props.rawDataBucket.grantRead(
      this.featureEngineeringFn
    );
    props.processedDataBucket.grantReadWrite(
      this.featureEngineeringFn
    );
    props.modelArtifactsBucket.grantRead(
      this.inferenceFn
    );
    props.processedDataBucket.grantRead(
      this.inferenceFn
    );
    props.rawDataBucket.grantRead(this.resultsFn);
    props.processedDataBucket.grantReadWrite(
      this.resultsFn
    );

    // ─────────────────────────────────────
    // EventBridge Schedules (unchanged)
    // ─────────────────────────────────────

    new events.Rule(this, 'IngestionSchedule', {
      ruleName: 'equine-ingestion-daily',
      schedule: events.Schedule.expression(
        'cron(0 11 * * ? *)'
      ),
      targets: [
        new targets.LambdaFunction(this.ingestionFn)
      ],
    });

    new events.Rule(
      this,
      'FeatureEngineeringSchedule',
      {
        ruleName: 'equine-feature-engineering-daily',
        schedule: events.Schedule.expression(
          'cron(0 12 * * ? *)'
        ),
        targets: [
          new targets.LambdaFunction(
            this.featureEngineeringFn
          )
        ],
      }
    );

    new events.Rule(this, 'InferenceSchedule', {
      ruleName: 'equine-inference-daily',
      schedule: events.Schedule.expression(
        'cron(30 12 * * ? *)'
      ),
      targets: [
        new targets.LambdaFunction(this.inferenceFn)
      ],
    });

    new events.Rule(this, 'ResultsSchedule', {
      ruleName: 'equine-results-daily',
      schedule: events.Schedule.expression(
        'cron(0 4 * * ? *)'
      ),
      targets: [
        new targets.LambdaFunction(this.resultsFn)
      ],
    });

    // ─────────────────────────────────────
    // HTTP API Gateway (unchanged)
    // ─────────────────────────────────────

    const httpApi = new apigwv2.HttpApi(
      this,
      'EquineApi',
      {
        apiName: 'equine-api',
        description:
          'HTTP API for Equine Equalizer predictions',
        corsPreflight: {
          allowOrigins: ['*'],
          allowMethods: [apigwv2.CorsHttpMethod.GET],
          allowHeaders: ['Content-Type'],
        },
      }
    );

    const inferenceIntegration =
      new apigwv2Integrations.HttpLambdaIntegration(
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
