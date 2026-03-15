import * as cdk from 'aws-cdk-lib/core';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';

export class StorageStack extends cdk.Stack {
  public readonly rawDataBucket: s3.Bucket;
  public readonly processedDataBucket: s3.Bucket;
  public readonly modelArtifactsBucket: s3.Bucket;
  public readonly frontendBucket: s3.Bucket;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Raw PP data files downloaded from Equibase
    this.rawDataBucket = new s3.Bucket(this, 'RawDataBucket', {
      bucketName: 'equine-raw-data',
      versioned: true,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
      lifecycleRules: [
        {
          transitions: [
            {
              storageClass: s3.StorageClass.GLACIER,
              transitionAfter: cdk.Duration.days(90),
            },
          ],
        },
      ],
    });

    // Feature-engineered datasets ready for training
    this.processedDataBucket = new s3.Bucket(this, 'ProcessedDataBucket', {
      bucketName: 'equine-processed-data',
      versioned: true,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    });

    // Trained XGBoost model files from SageMaker
    this.modelArtifactsBucket = new s3.Bucket(this, 'ModelArtifactsBucket', {
      bucketName: 'equine-model-artifacts',
      versioned: true,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    });

    // Built React static files served via CloudFront
    this.frontendBucket = new s3.Bucket(this, 'FrontendBucket', {
      bucketName: 'equine-frontend',
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    // CloudFormation outputs
    new cdk.CfnOutput(this, 'RawDataBucketArn', {
      value: this.rawDataBucket.bucketArn,
      exportName: 'EquineRawDataBucketArn',
    });
    new cdk.CfnOutput(this, 'RawDataBucketName', {
      value: this.rawDataBucket.bucketName,
      exportName: 'EquineRawDataBucketName',
    });
    new cdk.CfnOutput(this, 'ProcessedDataBucketArn', {
      value: this.processedDataBucket.bucketArn,
      exportName: 'EquineProcessedDataBucketArn',
    });
    new cdk.CfnOutput(this, 'ProcessedDataBucketName', {
      value: this.processedDataBucket.bucketName,
      exportName: 'EquineProcessedDataBucketName',
    });
    new cdk.CfnOutput(this, 'ModelArtifactsBucketArn', {
      value: this.modelArtifactsBucket.bucketArn,
      exportName: 'EquineModelArtifactsBucketArn',
    });
    new cdk.CfnOutput(this, 'ModelArtifactsBucketName', {
      value: this.modelArtifactsBucket.bucketName,
      exportName: 'EquineModelArtifactsBucketName',
    });
    new cdk.CfnOutput(this, 'FrontendBucketArn', {
      value: this.frontendBucket.bucketArn,
      exportName: 'EquineFrontendBucketArn',
    });
    new cdk.CfnOutput(this, 'FrontendBucketName', {
      value: this.frontendBucket.bucketName,
      exportName: 'EquineFrontendBucketName',
    });
  }
}
