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
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as iam from 'aws-cdk-lib/aws-iam';
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
  public readonly wrInferenceFn: lambda.Function;
  public readonly plInferenceFn: lambda.Function;
  public readonly lsInferenceFn: lambda.Function;

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
        timeout: cdk.Duration.minutes(15),
        memorySize: 1024,
        description:
          'Pulls daily race entries, parses chart PDFs',
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

    this.wrInferenceFn = new lambda.DockerImageFunction(
      this,
      'WRInferenceFunction',
      {
        ...sharedProps,
        functionName: 'equine-wr-inference',
        description: 'Win Rate model predictions',
        memorySize: 1024,
        code: lambda.DockerImageCode.fromImageAsset(
          projectRoot,
          { file: 'Dockerfile.wr-inference' }
        ),
      }
    );

    this.plInferenceFn = new lambda.DockerImageFunction(
      this,
      'PLInferenceFunction',
      {
        ...sharedProps,
        functionName: 'equine-pl-inference',
        description: 'P&L optimization model predictions',
        memorySize: 1024,
        code: lambda.DockerImageCode.fromImageAsset(
          projectRoot,
          { file: 'Dockerfile.pl-inference' }
        ),
      }
    );

    this.lsInferenceFn = new lambda.DockerImageFunction(
      this,
      'LSInferenceFunction',
      {
        ...sharedProps,
        functionName: 'equine-ls-inference',
        description: 'Longshot meta-model predictions',
        memorySize: 1024,
        code: lambda.DockerImageCode.fromImageAsset(
          projectRoot,
          { file: 'Dockerfile.ls-inference' }
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

    // Allow ingestion Lambda to invoke inference Lambda
    // for batch inference runs
    this.inferenceFn.grantInvoke(this.ingestionFn);

    props.rawDataBucket.grantReadWrite(
      this.ingestionFn
    );
    props.rawDataBucket.grantRead(
      this.featureEngineeringFn
    );
    props.processedDataBucket.grantReadWrite(
      this.featureEngineeringFn
    );
    props.modelArtifactsBucket.grantReadWrite(
      this.ingestionFn
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

    props.dbCluster.secret!.grantRead(this.wrInferenceFn);
    props.dbCluster.secret!.grantRead(this.plInferenceFn);
    props.dbCluster.secret!.grantRead(this.lsInferenceFn);

    props.modelArtifactsBucket.grantRead(this.wrInferenceFn);
    props.modelArtifactsBucket.grantRead(this.plInferenceFn);
    props.modelArtifactsBucket.grantRead(this.lsInferenceFn);

    props.processedDataBucket.grantRead(this.wrInferenceFn);
    props.processedDataBucket.grantRead(this.plInferenceFn);
    props.processedDataBucket.grantRead(this.lsInferenceFn);

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

    // NOTE: equine-feature-engineering-daily was deleted out-of-band
    // before 2026-04-28 (presumably to suppress its trigger). Recreated
    // as DISABLED so CFN reconciliation can grant the Lambda permission
    // resource without re-arming the schedule. Toggle State.ENABLED
    // when ready to resume.
    new events.Rule(
      this,
      'FeatureEngineeringSchedule',
      {
        ruleName: 'equine-feature-engineering-daily',
        schedule: events.Schedule.expression(
          'cron(0 12 * * ? *)'
        ),
        enabled: false,
        targets: [
          new targets.LambdaFunction(
            this.featureEngineeringFn
          )
        ],
      }
    );

    // NOTE: equine-inference-daily was deleted out-of-band before
    // 2026-04-28. Recreated as DISABLED — the per-model rules
    // (WR/PL/LS) cover the active inference paths.
    new events.Rule(this, 'InferenceSchedule', {
      ruleName: 'equine-inference-daily',
      schedule: events.Schedule.expression(
        'cron(30 12 * * ? *)'
      ),
      enabled: false,
      targets: [
        new targets.LambdaFunction(this.inferenceFn)
      ],
    });

    new events.Rule(this, 'WRInferenceSchedule', {
      ruleName: 'equine-wr-inference-daily',
      schedule: events.Schedule.expression(
        'cron(30 12 * * ? *)'
      ),
      targets: [
        new targets.LambdaFunction(this.wrInferenceFn)
      ],
    });

    new events.Rule(this, 'PLInferenceSchedule', {
      ruleName: 'equine-pl-inference-daily',
      schedule: events.Schedule.expression(
        'cron(35 12 * * ? *)'
      ),
      targets: [
        new targets.LambdaFunction(this.plInferenceFn)
      ],
    });

    new events.Rule(this, 'LSInferenceSchedule', {
      ruleName: 'equine-ls-inference-daily',
      schedule: events.Schedule.expression(
        'cron(40 12 * * ? *)'
      ),
      targets: [
        new targets.LambdaFunction(this.lsInferenceFn)
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
    // ECS Cluster + Training Task (Fargate)
    // ─────────────────────────────────────

    const cluster = new ecs.Cluster(this, 'EquineCluster', {
      vpc: props.vpc,
      clusterName: 'equine-cluster',
    });

    const trainingTaskDef = new ecs.FargateTaskDefinition(
      this,
      'TrainingTaskDef',
      {
        memoryLimitMiB: 4096,
        cpu: 2048,  // 2 vCPU
        family: 'equine-training',
      }
    );

    trainingTaskDef.addContainer('training', {
      image: ecs.ContainerImage.fromAsset(projectRoot, {
        file: 'Dockerfile.training',
      }),
      logging: ecs.LogDrivers.awsLogs({
        streamPrefix: 'training',
        logGroup: new logs.LogGroup(this, 'TrainingLogGroup', {
          logGroupName: '/ecs/equine-training',
          retention: logs.RetentionDays.TWO_WEEKS,
          removalPolicy: cdk.RemovalPolicy.DESTROY,
        }),
      }),
      environment: sharedEnv,
    });

    // Grant permissions to training task
    props.dbCluster.secret!.grantRead(trainingTaskDef.taskRole);
    props.modelArtifactsBucket.grantReadWrite(
      trainingTaskDef.taskRole
    );
    props.rawDataBucket.grantRead(trainingTaskDef.taskRole);

    // Training task uses same security group as Lambdas
    // (already allowed to connect to Aurora)

    new cdk.CfnOutput(this, 'TrainingTaskDefArn', {
      value: trainingTaskDef.taskDefinitionArn,
      exportName: 'EquineTrainingTaskDefArn',
    });
    new cdk.CfnOutput(this, 'EcsClusterName', {
      value: cluster.clusterName,
      exportName: 'EquineEcsClusterName',
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
          allowOrigins: [
            'https://d4nlmxq220z0z.cloudfront.net',
            'http://localhost:3000',
          ],
          allowMethods: [
            apigwv2.CorsHttpMethod.GET,
            apigwv2.CorsHttpMethod.POST,
            apigwv2.CorsHttpMethod.OPTIONS,
          ],
          allowHeaders: [
            'Content-Type',
            'Authorization',
          ],
          maxAge: cdk.Duration.days(1),
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
      path: '/cards/{date}/{track_code}',
      methods: [apigwv2.HttpMethod.GET],
      integration: inferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/health',
      methods: [apigwv2.HttpMethod.GET],
      integration: inferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/predictions/today',
      methods: [apigwv2.HttpMethod.GET],
      integration: inferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/predictions/value',
      methods: [apigwv2.HttpMethod.GET],
      integration: inferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/predictions/{date}',
      methods: [apigwv2.HttpMethod.GET],
      integration: inferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/predictions/{date}/{track_code}/{race_number}',
      methods: [apigwv2.HttpMethod.GET],
      integration: inferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/horses/{horse_id}/pps',
      methods: [apigwv2.HttpMethod.GET],
      integration: inferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/dashboard/metrics',
      methods: [apigwv2.HttpMethod.GET],
      integration: inferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/races/available-dates',
      methods: [apigwv2.HttpMethod.GET],
      integration: inferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/predictions/run',
      methods: [
        apigwv2.HttpMethod.GET,
        apigwv2.HttpMethod.POST,
      ],
      integration: inferenceIntegration,
    });

    const wrInferenceIntegration =
      new apigwv2Integrations.HttpLambdaIntegration(
        'WRInferenceIntegration',
        this.wrInferenceFn,
      );

    const plInferenceIntegration =
      new apigwv2Integrations.HttpLambdaIntegration(
        'PLInferenceIntegration',
        this.plInferenceFn,
      );

    const lsInferenceIntegration =
      new apigwv2Integrations.HttpLambdaIntegration(
        'LSInferenceIntegration',
        this.lsInferenceFn,
      );

    httpApi.addRoutes({
      path: '/wr/health',
      methods: [apigwv2.HttpMethod.GET],
      integration: wrInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/wr/predictions/today',
      methods: [apigwv2.HttpMethod.GET],
      integration: wrInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/wr/predictions/value',
      methods: [apigwv2.HttpMethod.GET],
      integration: wrInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/wr/predictions/{date}',
      methods: [apigwv2.HttpMethod.GET],
      integration: wrInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/wr/predictions/{date}/compare',
      methods: [apigwv2.HttpMethod.GET],
      integration: wrInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/wr/predictions/{date}/{track_code}/{race_number}',
      methods: [apigwv2.HttpMethod.GET],
      integration: wrInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/wr/predictions/run',
      methods: [apigwv2.HttpMethod.GET, apigwv2.HttpMethod.POST],
      integration: wrInferenceIntegration,
    });
    // Stream E2 — track-record aggregates
    httpApi.addRoutes({
      path: '/wr/predictions/track-record',
      methods: [apigwv2.HttpMethod.GET],
      integration: wrInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/wr/predictions/track-record-by-style',
      methods: [apigwv2.HttpMethod.GET],
      integration: wrInferenceIntegration,
    });

    httpApi.addRoutes({
      path: '/pl/health',
      methods: [apigwv2.HttpMethod.GET],
      integration: plInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/pl/predictions/today',
      methods: [apigwv2.HttpMethod.GET],
      integration: plInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/pl/predictions/value',
      methods: [apigwv2.HttpMethod.GET],
      integration: plInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/pl/predictions/{date}',
      methods: [apigwv2.HttpMethod.GET],
      integration: plInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/pl/predictions/{date}/{track_code}/{race_number}',
      methods: [apigwv2.HttpMethod.GET],
      integration: plInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/pl/predictions/run',
      methods: [apigwv2.HttpMethod.GET, apigwv2.HttpMethod.POST],
      integration: plInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/pl/predictions/track-record',
      methods: [apigwv2.HttpMethod.GET],
      integration: plInferenceIntegration,
    });

    httpApi.addRoutes({
      path: '/ls/health',
      methods: [apigwv2.HttpMethod.GET],
      integration: lsInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/ls/predictions/today',
      methods: [apigwv2.HttpMethod.GET],
      integration: lsInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/ls/predictions/alerts',
      methods: [apigwv2.HttpMethod.GET],
      integration: lsInferenceIntegration,
    });
    // Frontend's getLSAlerts hits /longshots — Lambda handler matches
    // /longshots, so add it to API Gateway too.
    httpApi.addRoutes({
      path: '/ls/predictions/longshots',
      methods: [apigwv2.HttpMethod.GET],
      integration: lsInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/ls/predictions/{date}',
      methods: [apigwv2.HttpMethod.GET],
      integration: lsInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/ls/predictions/{date}/{track_code}/{race_number}',
      methods: [apigwv2.HttpMethod.GET],
      integration: lsInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/ls/predictions/run',
      methods: [apigwv2.HttpMethod.GET, apigwv2.HttpMethod.POST],
      integration: lsInferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/ls/predictions/track-record',
      methods: [apigwv2.HttpMethod.GET],
      integration: lsInferenceIntegration,
    });

    new cdk.CfnOutput(this, 'ApiUrl', {
      value: httpApi.apiEndpoint,
      exportName: 'EquineApiUrl',
    });
  }
}
