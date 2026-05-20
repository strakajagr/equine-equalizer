import * as path from 'path';
import * as cdk from 'aws-cdk-lib/core';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as lambdaDestinations
  from 'aws-cdk-lib/aws-lambda-destinations';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as apigwv2 from 'aws-cdk-lib/aws-apigatewayv2';
import * as apigwv2Integrations
  from 'aws-cdk-lib/aws-apigatewayv2-integrations';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as cloudwatch from 'aws-cdk-lib/aws-cloudwatch';
import * as cwActions
  from 'aws-cdk-lib/aws-cloudwatch-actions';
import * as sns from 'aws-cdk-lib/aws-sns';
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
    // SP-T1-PHASE-B Daily report email Lambdas
    // ─────────────────────────────────────
    // Reuse Dockerfile.inference image; override CMD per Lambda.
    // CDK builds image once, both Lambdas reference same ECR digest.
    //
    // NB: NO VPC config — matches production inference Lambda pattern.
    // Email Lambdas reach RDS via the cluster's public endpoint + Secrets
    // Manager via public internet. Initial deploy attempted VPC config from
    // sharedProps but hung on Secrets Manager Connect timeout (private
    // subnets lack route to Secrets Manager). Substrate-pragmatic fix:
    // bypass sharedProps' vpc/securityGroups for these Lambdas.

    const dashboardUrl =
      'https://d4nlmxq220z0z.cloudfront.net/reports/daily';
    const recipientEmail = 'tonyragano@gmail.com';
    const senderEmail = 'tonyragano@gmail.com';

    const dailyMorningEmailFn = new lambda.DockerImageFunction(
      this,
      'DailyMorningEmailFunction',
      {
        functionName: 'equine-daily-morning-email',
        description:
          'Generates daily strategy report at 07:00 ET; persists recs; emails Tony',
        memorySize: 2048,
        timeout: cdk.Duration.minutes(10),
        environment: {
          ...sharedEnv,
          RECIPIENT_EMAIL: recipientEmail,
          SENDER_EMAIL: senderEmail,
          DASHBOARD_URL: dashboardUrl,
        },
        code: lambda.DockerImageCode.fromImageAsset(
          projectRoot,
          {
            file: 'Dockerfile.inference',
            cmd: ['lambdas/daily_morning_email/handler.handler'],
          }
        ),
      }
    );

    const dailyEveningEmailFn = new lambda.DockerImageFunction(
      this,
      'DailyEveningEmailFunction',
      {
        functionName: 'equine-daily-evening-email',
        description:
          'Computes daily P&L at 23:30 ET; persists to strategy_pnl; emails Tony',
        memorySize: 2048,
        timeout: cdk.Duration.minutes(10),
        environment: {
          ...sharedEnv,
          RECIPIENT_EMAIL: recipientEmail,
          SENDER_EMAIL: senderEmail,
          DASHBOARD_URL: dashboardUrl,
        },
        code: lambda.DockerImageCode.fromImageAsset(
          projectRoot,
          {
            file: 'Dockerfile.inference',
            cmd: ['lambdas/daily_evening_email/handler.handler'],
          }
        ),
      }
    );

    // SES send permissions for both email Lambdas
    [dailyMorningEmailFn, dailyEveningEmailFn].forEach(fn => {
      fn.addToRolePolicy(
        new iam.PolicyStatement({
          actions: ['ses:SendEmail', 'ses:SendRawEmail'],
          resources: ['*'],
        })
      );
      // DB secret read
      props.dbCluster.secret!.grantRead(fn);
    });

    // ─────────────────────────────────────
    // SP-SUBSTRATE-HEALTH-MONITOR Lambda
    // ─────────────────────────────────────
    // Runs 5 min before morning report; surfaces RED/YELLOW/GREEN status
    // across chart pipeline, HRN results, past_performances, workouts,
    // wr_predictions, cron firings, Lambda error counts, model artifact age.
    // NO VPC config — matches production pattern (Phase B VPC drift lesson).

    const substrateHealthMonitorFn = new lambda.DockerImageFunction(
      this,
      'SubstrateHealthMonitorFunction',
      {
        functionName: 'equine-substrate-health-monitor',
        description:
          'Daily substrate health check; emails Tony 5 min before morning report',
        memorySize: 1024,
        timeout: cdk.Duration.minutes(5),
        environment: {
          ...sharedEnv,
          RECIPIENT_EMAIL: recipientEmail,
          SENDER_EMAIL: senderEmail,
        },
        code: lambda.DockerImageCode.fromImageAsset(
          projectRoot,
          { file: 'Dockerfile.health-monitor' }
        ),
      }
    );

    // IAM: secrets, SES, S3, CloudWatch metrics, Logs filter
    substrateHealthMonitorFn.addToRolePolicy(
      new iam.PolicyStatement({
        actions: ['ses:SendEmail', 'ses:SendRawEmail'],
        resources: ['*'],
      })
    );
    substrateHealthMonitorFn.addToRolePolicy(
      new iam.PolicyStatement({
        actions: [
          's3:ListBucket', 's3:GetObject',
          'cloudwatch:GetMetricStatistics',
          'logs:FilterLogEvents', 'logs:DescribeLogGroups',
        ],
        resources: ['*'],
      })
    );
    props.dbCluster.secret!.grantRead(substrateHealthMonitorFn);

    new events.Rule(this, 'SubstrateHealthMonitorRule', {
      ruleName: 'equine-substrate-health-cron',
      description:
        'Substrate health check 5 min before morning report (10:55 UTC = 06:55 EDT)',
      schedule: events.Schedule.expression('cron(55 10 * * ? *)'),
      targets: [new targets.LambdaFunction(substrateHealthMonitorFn)],
    });

    // ─────────────────────────────────────
    // IAM Permissions (unchanged)
    // ─────────────────────────────────────

    props.dbCluster.secret!.grantRead(
      this.ingestionFn
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
    // SP-T1-PHASE-B EventBridge crons for email Lambdas
    // ─────────────────────────────────────

    new events.Rule(this, 'DailyMorningReportSchedule', {
      ruleName: 'equine-morning-report-cron',
      description: 'Daily strategy report at 07:00 ET (11:00 UTC EDT / 12:00 UTC EST)',
      schedule: events.Schedule.expression('cron(0 11 * * ? *)'),
      targets: [
        new targets.LambdaFunction(dailyMorningEmailFn),
      ],
    });

    new events.Rule(this, 'DailyEveningPnLSchedule', {
      ruleName: 'equine-evening-pnl-cron',
      description: 'Daily P&L summary at 23:30 ET (03:30 UTC next-day EDT / 04:30 UTC EST)',
      schedule: events.Schedule.expression('cron(30 3 * * ? *)'),
      targets: [
        new targets.LambdaFunction(dailyEveningEmailFn),
      ],
    });

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

    // FeatureEngineeringSchedule rule + FeatureEngineeringFunction Lambda
    // removed at E4 Step 3 Phase 2 A4.3 (E3 absorption into Path A cdk
    // deploy). Feature-engineering cohort retired per E3 narrow-scope
    // ratification. Backend Python module backend/services/feature_engineering_service.py
    // retained — load-bearing shared module for WR/PL/LS inference Lambdas.

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

    new events.Rule(this, 'SpeedFiguresSchedule', {
      ruleName: 'equine-speed-figures-daily',
      schedule: events.Schedule.expression(
        'cron(0 9 * * ? *)'
      ),
      targets: [
        new targets.LambdaFunction(
          this.ingestionFn,
          {
            event: events.RuleTargetInput.fromObject({
              action: 'compute_speed_figures',
            }),
          }
        ),
      ],
    });

    new events.Rule(this, 'TripFlagsSchedule', {
      ruleName: 'equine-trip-flags-daily',
      schedule: events.Schedule.expression(
        'cron(15 9 * * ? *)'
      ),
      targets: [
        new targets.LambdaFunction(
          this.ingestionFn,
          {
            event: events.RuleTargetInput.fromObject({
              action: 'backfill_trip_flags',
            }),
          }
        ),
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

    // SP-T1-PHASE-B daily report routes
    httpApi.addRoutes({
      path: '/api/reports/daily/{race_date}',
      methods: [apigwv2.HttpMethod.GET],
      integration: inferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/api/reports/strategy/list',
      methods: [apigwv2.HttpMethod.GET],
      integration: inferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/api/reports/strategy/{strategy_name}/history',
      methods: [apigwv2.HttpMethod.GET],
      integration: inferenceIntegration,
    });
    httpApi.addRoutes({
      path: '/api/reports/strategy_pnl/range',
      methods: [apigwv2.HttpMethod.GET],
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

    // ═══════════════════════════════════════════════════════════════════
    // E4 Phase A reconciliation patches (v3-patched-d AO-1 + AO-4 + Phase A-prime
    // DLQ wiring + A.5 inference DLQ + A.5-ext NYRA workouts DLQ + A.5-α
    // predictions-deficit alarms + Dispatch 1 outcome alarms + OCRC Fix 5
    // invocation-class alarms + Entries-HRN-gating CC composite alarm).
    //
    // All declarations below are SUBSTRATE-VERBATIM matches to current AWS state.
    // No semantic changes. cdk diff target: zero changes after CloudFormation
    // resource-import workflow (aws cloudformation create-change-set
    // --change-set-type IMPORT) brings existing CLI-only resources under
    // stack management. See E4 Step 3 dispatch for import procedure.
    //
    // Substrate citation: docs/operations/PHASE_A_HANDOFF_2026-05-12.md
    //   § 1.2 (6-Lambda DLQ coverage final tally)
    //   § 1.3 (29-alarm inventory)
    //   § 2.10 (predictions-deficit alarm pattern math expression)
    // ═══════════════════════════════════════════════════════════════════

    // ───────────────────────────────────────
    // SQS DLQ + depth alarm (Phase A-prime)
    // ───────────────────────────────────────

    const asyncFailureDlq = new sqs.Queue(
      this, 'AsyncFailureDlq',
      {
        queueName: 'equine-async-failure-dlq',
        retentionPeriod: cdk.Duration.days(14),
      }
    );

    // Existing SNS topic for alarm actions (CLI-only at Phase A baseline;
    // referenced by ARN; resource import required for CDK management).
    const alertTopic = sns.Topic.fromTopicArn(
      this, 'AlertTopic',
      'arn:aws:sns:us-east-1:584812014683:equine-equalizer-alerts'
    );

    new cloudwatch.Alarm(
      this, 'AsyncDlqMessagesPresent',
      {
        alarmName: 'equine-async-dlq-messages-present',
        metric: new cloudwatch.Metric({
          namespace: 'AWS/SQS',
          metricName: 'ApproximateNumberOfMessagesVisible',
          dimensionsMap: {
            QueueName: 'equine-async-failure-dlq',
          },
          statistic: 'Maximum',
          period: cdk.Duration.seconds(300),
        }),
        threshold: 0,
        comparisonOperator:
          cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
        evaluationPeriods: 1,
        treatMissingData:
          cloudwatch.TreatMissingData.NOT_BREACHING,
      }
    ).addAlarmAction(new cwActions.SnsAction(alertTopic));

    // ───────────────────────────────────────
    // 6-Lambda async event-invoke-config + AsyncDLQSend IAM policies
    // Step ordering per AWS API validation discipline
    // (data_pipeline_bible:4.5; AUDIT_METHODOLOGY:4.30):
    // IAM grant must precede event-invoke-config. CDK construct
    // dependency graph handles automatically — verify post-deploy.
    // ───────────────────────────────────────

    const asyncDlqStatement = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: ['sqs:SendMessage'],
      resources: [asyncFailureDlq.queueArn],
    });

    const dlqAttachedLambdas: Array<{
      fn: lambda.Function;
      id: string;
    }> = [
      { fn: this.ingestionFn, id: 'Ingestion' },
      { fn: this.resultsFn, id: 'Results' },
      { fn: this.wrInferenceFn, id: 'WRInference' },
      { fn: this.plInferenceFn, id: 'PLInference' },
      { fn: this.lsInferenceFn, id: 'LSInference' },
    ];

    // E4 Step 3 Phase 1.5 refactor: L2 iam.Policy → L1 iam.CfnRolePolicy
    // for CloudFormation resource-import compatibility. Synthesizes as
    // AWS::IAM::RolePolicy (inline policy on role) which IS resource-import-
    // compatible per AWS::CloudFormation::ResourceTypeSchemaRegistry
    // (primaryIdentifier: [PolicyName, RoleName]; READ handler present).
    // L2 iam.Policy synthesized as AWS::IAM::Policy which requires standalone
    // policy ARN for import — incompatible with inline policies on existing
    // CLI-deployed roles. PolicyName 'AsyncDLQSend' verbatim per Phase A-prime
    // / A.5 / A.5-ext CLI deployment substrate; substrate-verified via
    // `aws iam list-role-policies` returning 'AsyncDLQSend' on all 5 roles.
    for (const { fn, id } of dlqAttachedLambdas) {
      new iam.CfnRolePolicy(this, `${id}AsyncDLQSend`, {
        policyName: 'AsyncDLQSend',
        roleName: fn.role!.roleName,
        policyDocument: {
          Version: '2012-10-17',
          Statement: [
            {
              Effect: 'Allow',
              Action: 'sqs:SendMessage',
              Resource: asyncFailureDlq.queueArn,
            },
          ],
        },
      });
      fn.configureAsyncInvoke({
        onFailure: new lambdaDestinations.SqsDestination(
          asyncFailureDlq
        ),
        retryAttempts: 2,
        maxEventAge: cdk.Duration.seconds(3600),
      });
    }

    // ───────────────────────────────────────
    // CLI-only Lambda imports — adopted via fromFunctionAttributes.
    // These Lambdas were deployed via AWS CLI before E4 reconciliation.
    // CDK references them by ARN for alarm + rule wiring; full CDK
    // ownership requires CloudFormation resource import.
    // ───────────────────────────────────────

    const nyraWorkoutsFn = lambda.Function.fromFunctionAttributes(
      this, 'NyraWorkoutsFn',
      {
        functionArn:
          'arn:aws:lambda:us-east-1:584812014683:function:equine-nyra-workouts',
        sameEnvironment: true,
      }
    );

    const entriesTracksPublisherFn = lambda.Function.fromFunctionAttributes(
      this, 'EntriesTracksPublisherFn',
      {
        functionArn:
          'arn:aws:lambda:us-east-1:584812014683:function:equine-entries-tracks-publisher',
        sameEnvironment: true,
      }
    );

    const outcomeMetricPublisherFn = lambda.Function.fromFunctionAttributes(
      this, 'OutcomeMetricPublisherFn',
      {
        functionArn:
          'arn:aws:lambda:us-east-1:584812014683:function:equine-outcome-metric-publisher',
        sameEnvironment: true,
      }
    );

    // ───────────────────────────────────────
    // NYRA workouts Lambda DLQ wiring (A.5-ext 2026-05-12).
    // Cannot use configureAsyncInvoke on imported Function (CDK
    // limitation); declared via CfnEventInvokeConfig L1 resource.
    // ───────────────────────────────────────

    new lambda.CfnEventInvokeConfig(
      this, 'NyraWorkoutsAsyncInvoke',
      {
        functionName: 'equine-nyra-workouts',
        qualifier: '$LATEST',
        maximumRetryAttempts: 2,
        maximumEventAgeInSeconds: 3600,
        destinationConfig: {
          onFailure: {
            destination: asyncFailureDlq.queueArn,
          },
        },
      }
    );

    // ───────────────────────────────────────
    // EventBridge rules — sibling + publisher + outcome
    // ───────────────────────────────────────

    new events.Rule(this, 'NyraWorkoutsSchedule', {
      ruleName: 'equine-nyra-workouts-daily',
      schedule: events.Schedule.expression(
        'cron(0 16 * * ? *)'
      ),
      targets: [
        new targets.LambdaFunction(nyraWorkoutsFn),
      ],
    });

    // A4.2.5 pre-fix: preserve operator-CLI-set target Id 'etp-daily'
    // to match AWS state post-import (resolves MODIFIED drift on
    // Targets/0/Id detected at SP-A4 Phase A4.2). CDK auto-generates
    // 'Target0'; operator-set value preserved via L1 CfnRule property
    // override per Banking Refinement 7 third sub-class option (c):
    // leave operator-CLI-set values via CDK property override constructs.
    const entriesTracksPublisherScheduleRule = new events.Rule(
      this, 'EntriesTracksPublisherSchedule', {
        ruleName: 'equine-entries-tracks-publisher-daily',
        schedule: events.Schedule.expression(
          'cron(15 11 * * ? *)'
        ),
        targets: [
          new targets.LambdaFunction(
            entriesTracksPublisherFn
          ),
        ],
      }
    );
    (entriesTracksPublisherScheduleRule.node.defaultChild as events.CfnRule)
      .addPropertyOverride('Targets.0.Id', 'etp-daily');

    new events.Rule(this, 'OutcomeResultsCheckSchedule', {
      ruleName: 'equine-outcome-results-check',
      schedule: events.Schedule.expression(
        'cron(0 6 * * ? *)'
      ),
      targets: [
        new targets.LambdaFunction(
          outcomeMetricPublisherFn,
          {
            event: events.RuleTargetInput.fromObject({
              metric: 'results',
            }),
          }
        ),
      ],
    });

    new events.Rule(this, 'OutcomeWorkoutsCheckSchedule', {
      ruleName: 'equine-outcome-workouts-check',
      schedule: events.Schedule.expression(
        'cron(0 9 * * ? *)'
      ),
      targets: [
        new targets.LambdaFunction(
          outcomeMetricPublisherFn,
          {
            event: events.RuleTargetInput.fromObject({
              metric: 'workouts',
            }),
          }
        ),
      ],
    });

    // RETIRED rule (entries outcome path decommissioned at
    // Entries-HRN-gating CC 2026-05-12 BEL slug verification cycle).
    // CDK declares DISABLED to match AWS substrate; no targets
    // declared (target was removed at decommission).
    new events.Rule(this, 'OutcomeEntriesCheckSchedule', {
      ruleName: 'equine-outcome-entries-check',
      schedule: events.Schedule.expression(
        'cron(30 12 * * ? *)'
      ),
      enabled: false,
    });

    // ───────────────────────────────────────
    // CloudWatch alarm helper (reduces 27-alarm boilerplate)
    // ───────────────────────────────────────

    const lambdaErrorAlarm = (
      id: string,
      alarmName: string,
      functionName: string
    ): cloudwatch.Alarm => {
      const a = new cloudwatch.Alarm(this, id, {
        alarmName,
        metric: new cloudwatch.Metric({
          namespace: 'AWS/Lambda',
          metricName: 'Errors',
          dimensionsMap: { FunctionName: functionName },
          statistic: 'Sum',
          period: cdk.Duration.seconds(300),
        }),
        threshold: 0,
        comparisonOperator:
          cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
        evaluationPeriods: 1,
        treatMissingData:
          cloudwatch.TreatMissingData.NOT_BREACHING,
      });
      a.addAlarmAction(new cwActions.SnsAction(alertTopic));
      return a;
    };

    const lambdaThrottleAlarm = (
      id: string,
      alarmName: string,
      functionName: string
    ): cloudwatch.Alarm => {
      const a = new cloudwatch.Alarm(this, id, {
        alarmName,
        metric: new cloudwatch.Metric({
          namespace: 'AWS/Lambda',
          metricName: 'Throttles',
          dimensionsMap: { FunctionName: functionName },
          statistic: 'Sum',
          period: cdk.Duration.seconds(300),
        }),
        threshold: 0,
        comparisonOperator:
          cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
        evaluationPeriods: 1,
        treatMissingData:
          cloudwatch.TreatMissingData.NOT_BREACHING,
      });
      a.addAlarmAction(new cwActions.SnsAction(alertTopic));
      return a;
    };

    const invocationsAbsenceAlarm = (
      id: string,
      alarmName: string,
      functionName: string
    ): cloudwatch.Alarm => {
      const a = new cloudwatch.Alarm(this, id, {
        alarmName,
        metric: new cloudwatch.Metric({
          namespace: 'AWS/Lambda',
          metricName: 'Invocations',
          dimensionsMap: { FunctionName: functionName },
          statistic: 'Sum',
          period: cdk.Duration.seconds(86400),
        }),
        threshold: 1,
        comparisonOperator:
          cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
        evaluationPeriods: 1,
        treatMissingData:
          cloudwatch.TreatMissingData.BREACHING,
      });
      a.addAlarmAction(new cwActions.SnsAction(alertTopic));
      return a;
    };

    const cronAbsenceAlarm = (
      id: string,
      alarmName: string,
      ruleName: string
    ): cloudwatch.Alarm => {
      const a = new cloudwatch.Alarm(this, id, {
        alarmName,
        metric: new cloudwatch.Metric({
          namespace: 'AWS/Events',
          metricName: 'Invocations',
          dimensionsMap: { RuleName: ruleName },
          statistic: 'Sum',
          period: cdk.Duration.seconds(86400),
        }),
        threshold: 1,
        comparisonOperator:
          cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
        evaluationPeriods: 1,
        treatMissingData:
          cloudwatch.TreatMissingData.BREACHING,
      });
      a.addAlarmAction(new cwActions.SnsAction(alertTopic));
      return a;
    };

    // ───────────────────────────────────────
    // 22 OCRC Fix 5 invocation-class alarms
    // ───────────────────────────────────────

    // Errors (8 Lambdas): NOTE per E3 narrow-scope v3-patched-e —
    // equine-feature-engineering-{errors,throttles} are E3 Step 2
    // deletion targets; commented out post-E3-execution.
    lambdaErrorAlarm('IngestionErrorsAlarm',
      'equine-ingestion-errors', 'equine-ingestion');
    lambdaErrorAlarm('ResultsErrorsAlarm',
      'equine-results-errors', 'equine-results');
    lambdaErrorAlarm('NyraWorkoutsErrorsAlarm',
      'equine-nyra-workouts-errors', 'equine-nyra-workouts');
    lambdaErrorAlarm('WRInferenceErrorsAlarm',
      'equine-wr-inference-errors', 'equine-wr-inference');
    lambdaErrorAlarm('PLInferenceErrorsAlarm',
      'equine-pl-inference-errors', 'equine-pl-inference');
    lambdaErrorAlarm('LSInferenceErrorsAlarm',
      'equine-ls-inference-errors', 'equine-ls-inference');
    // RC-2 v3-patched-e: equine-inference-errors is PRODUCTION-CLASS
    // (API handler), NOT orphan-watching. Retained.
    lambdaErrorAlarm('InferenceErrorsAlarm',
      'equine-inference-errors', 'equine-inference');
    // FeatureEngineeringErrorsAlarm removed at A4.3 (E3 absorption).

    // Throttles (7 Lambdas; same pattern post-E3 removal):
    lambdaThrottleAlarm('IngestionThrottlesAlarm',
      'equine-ingestion-throttles', 'equine-ingestion');
    lambdaThrottleAlarm('ResultsThrottlesAlarm',
      'equine-results-throttles', 'equine-results');
    lambdaThrottleAlarm('NyraWorkoutsThrottlesAlarm',
      'equine-nyra-workouts-throttles', 'equine-nyra-workouts');
    lambdaThrottleAlarm('WRInferenceThrottlesAlarm',
      'equine-wr-inference-throttles', 'equine-wr-inference');
    lambdaThrottleAlarm('PLInferenceThrottlesAlarm',
      'equine-pl-inference-throttles', 'equine-pl-inference');
    lambdaThrottleAlarm('LSInferenceThrottlesAlarm',
      'equine-ls-inference-throttles', 'equine-ls-inference');
    lambdaThrottleAlarm('InferenceThrottlesAlarm',
      'equine-inference-throttles', 'equine-inference');
    // FeatureEngineeringThrottlesAlarm removed at A4.3 (E3 absorption).

    // Invocations-absence (3):
    invocationsAbsenceAlarm(
      'IngestionInvocationsAbsenceAlarm',
      'equine-ingestion-invocations-absence',
      'equine-ingestion'
    );
    invocationsAbsenceAlarm(
      'ResultsInvocationsAbsenceAlarm',
      'equine-results-invocations-absence',
      'equine-results'
    );
    invocationsAbsenceAlarm(
      'NyraWorkoutsInvocationsAbsenceAlarm',
      'equine-nyra-workouts-invocations-absence',
      'equine-nyra-workouts'
    );

    // EventBridge cron-absence (3):
    cronAbsenceAlarm(
      'IngestionCronAbsenceAlarm',
      'equine-ingestion-daily-cron-absence',
      'equine-ingestion-daily'
    );
    cronAbsenceAlarm(
      'FetchResultsCronAbsenceAlarm',
      'equine-fetch-results-nightly-cron-absence',
      'equine-fetch-results-nightly'
    );
    cronAbsenceAlarm(
      'NyraWorkoutsCronAbsenceAlarm',
      'equine-nyra-workouts-daily-cron-absence',
      'equine-nyra-workouts-daily'
    );

    // ───────────────────────────────────────
    // Outcome-class alarms (Dispatch 1, 2026-05-11):
    // ───────────────────────────────────────

    new cloudwatch.Alarm(this, 'ResultsRowsWrittenTodayAlarm', {
      alarmName: 'equine-results-rows-written-today',
      metric: new cloudwatch.Metric({
        namespace: 'EquineEqualizer/Outcomes',
        metricName: 'ResultsRowsToday',
        statistic: 'Maximum',
        period: cdk.Duration.seconds(86400),
      }),
      threshold: 1,
      comparisonOperator:
        cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
      evaluationPeriods: 1,
      treatMissingData: cloudwatch.TreatMissingData.BREACHING,
    }).addAlarmAction(new cwActions.SnsAction(alertTopic));

    new cloudwatch.Alarm(this, 'WorkoutsObjectsWrittenTodayAlarm', {
      alarmName: 'equine-workouts-objects-written-today',
      metric: new cloudwatch.Metric({
        namespace: 'EquineEqualizer/Outcomes',
        metricName: 'WorkoutsObjectsToday',
        statistic: 'Maximum',
        period: cdk.Duration.seconds(86400),
      }),
      threshold: 1,
      comparisonOperator:
        cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
      evaluationPeriods: 1,
      treatMissingData: cloudwatch.TreatMissingData.BREACHING,
    }).addAlarmAction(new cwActions.SnsAction(alertTopic));

    // ───────────────────────────────────────
    // Composite HRN-gated entries alarm (2026-05-12 CC):
    // Math expression IF(m1 > 0, m1 - m2, 0) > 0
    // ───────────────────────────────────────

    const expectedQualifyingTracks = new cloudwatch.Metric({
      namespace: 'EquineEqualizer/Ingestion',
      metricName: 'EquineExpectedQualifyingTracksToday',
      statistic: 'Maximum',
      period: cdk.Duration.seconds(300),
    });
    const actualQualifyingTracks = new cloudwatch.Metric({
      namespace: 'EquineEqualizer/Ingestion',
      metricName:
        'EquineActualQualifyingTracksWithEntriesToday',
      statistic: 'Maximum',
      period: cdk.Duration.seconds(300),
    });

    new cloudwatch.Alarm(
      this, 'EntriesQualifyingTracksMissingAlarm',
      {
        alarmName: 'equine-entries-qualifying-tracks-missing',
        metric: new cloudwatch.MathExpression({
          expression: 'IF(m1 > 0, m1 - m2, 0)',
          usingMetrics: {
            m1: expectedQualifyingTracks,
            m2: actualQualifyingTracks,
          },
          period: cdk.Duration.seconds(300),
        }),
        threshold: 0,
        comparisonOperator:
          cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
        evaluationPeriods: 1,
        // Publisher fires once daily (cron 11:15 UTC); every other 5-min window
        // has no datapoint. BREACHING produced chronic false-positives (5+
        // consecutive days OK→ALARM→OK at 11:16/11:31). notBreaching keeps the
        // alarm honest: only fires when actual qualifying tracks < expected.
        treatMissingData:
          cloudwatch.TreatMissingData.NOT_BREACHING,
      }
    ).addAlarmAction(new cwActions.SnsAction(alertTopic));

    // ───────────────────────────────────────
    // Workout scraper cliff detector (Bug #7 Phase 5, 2026-05-16):
    // Daily delta alarm — would have surfaced HRN-scraper-stopped-working
    // weeks earlier when workout-count plummeted in late 2023. Coherent trio
    // per § 4.15: daily publisher (Equibase 03:00 UTC + NYRA 12:00 UTC) ×
    // 24h evaluation period × notBreaching missing-data treatment.
    //
    // Publishes DailyWorkoutCount metric from the ingestion Lambda after
    // load_workouts_from_s3 completes; alarms when today's count is <50%
    // of trailing-7-day average.
    // ───────────────────────────────────────
    const dailyWorkoutCountMetric = new cloudwatch.Metric({
      namespace: 'EquineEqualizer/Ingestion',
      metricName: 'DailyWorkoutCount',
      statistic: 'Sum',
      period: cdk.Duration.hours(24),
    });

    new cloudwatch.Alarm(this, 'WorkoutScraperCliffDetector', {
      alarmName: 'equine-workout-scraper-cliff-detector',
      alarmDescription:
        'Daily workout count <50% of trailing-7-day average; ' +
        'possible scraper regression. Would have surfaced ' +
        '2023-12 HRN-scraper-stopped + 2026-05 OP-meet-closed ' +
        'pattern signals ~2 weeks earlier than chart anomalies.',
      metric: new cloudwatch.MathExpression({
        expression: 'IF(m1 < 0.5 * AVG(METRICS()), 1, 0)',
        usingMetrics: { m1: dailyWorkoutCountMetric },
        period: cdk.Duration.hours(24),
      }),
      threshold: 0,
      comparisonOperator:
        cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
      evaluationPeriods: 1,
      treatMissingData: cloudwatch.TreatMissingData.NOT_BREACHING,
    }).addAlarmAction(new cwActions.SnsAction(alertTopic));

    // ───────────────────────────────────────
    // Predictions-deficit composite alarms (A.5; 3 per-pipeline):
    // Math expression IF(m1 > 0, m1 - m2, 0) > 0
    // m1 = Expected, m2 = Actual, namespace EquineEqualizer/Inference
    // ───────────────────────────────────────

    const predictionsDeficitAlarm = (
      id: string,
      alarmName: string,
      expectedMetricName: string,
      actualMetricName: string
    ): cloudwatch.Alarm => {
      const expected = new cloudwatch.Metric({
        namespace: 'EquineEqualizer/Inference',
        metricName: expectedMetricName,
        statistic: 'Maximum',
        period: cdk.Duration.seconds(300),
      });
      const actual = new cloudwatch.Metric({
        namespace: 'EquineEqualizer/Inference',
        metricName: actualMetricName,
        statistic: 'Maximum',
        period: cdk.Duration.seconds(300),
      });
      const a = new cloudwatch.Alarm(this, id, {
        alarmName,
        metric: new cloudwatch.MathExpression({
          expression: 'IF(m1 > 0, m1 - m2, 0)',
          usingMetrics: { m1: expected, m2: actual },
          period: cdk.Duration.seconds(300),
        }),
        threshold: 0,
        comparisonOperator:
          cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
        evaluationPeriods: 1,
        treatMissingData:
          cloudwatch.TreatMissingData.BREACHING,
      });
      a.addAlarmAction(new cwActions.SnsAction(alertTopic));
      return a;
    };

    predictionsDeficitAlarm(
      'WRPredictionsDeficitAlarm',
      'equine-wr-predictions-deficit',
      'EquineExpectedWRPredictionsToday',
      'EquineActualWRPredictionsToday'
    );
    predictionsDeficitAlarm(
      'PLPredictionsDeficitAlarm',
      'equine-pl-predictions-deficit',
      'EquineExpectedPLPredictionsToday',
      'EquineActualPLPredictionsToday'
    );
    predictionsDeficitAlarm(
      'LSPredictionsDeficitAlarm',
      'equine-ls-predictions-deficit',
      'EquineExpectedLSPredictionsToday',
      'EquineActualLSPredictionsToday'
    );

    // ═══════════════════════════════════════════════════════════════════
    // End of E4 reconciliation patches.
    // ═══════════════════════════════════════════════════════════════════
  }
}
