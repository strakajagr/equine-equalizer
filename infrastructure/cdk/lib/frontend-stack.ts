import * as cdk from 'aws-cdk-lib/core';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';

export class FrontendStack extends cdk.Stack {
  public readonly distribution: cloudfront.Distribution;
  public readonly frontendBucket: s3.Bucket;

  constructor(
    scope: Construct,
    id: string,
    props?: cdk.StackProps
  ) {
    super(scope, id, props);

    // Frontend bucket lives here, not in StorageStack.
    // It is a frontend concern, not a data concern.
    this.frontendBucket = new s3.Bucket(
      this,
      'FrontendBucket',
      {
        bucketName: 'equine-frontend',
        blockPublicAccess:
          s3.BlockPublicAccess.BLOCK_ALL,
        removalPolicy: cdk.RemovalPolicy.DESTROY,
        autoDeleteObjects: true,
      }
    );

    // OAC — no cross-stack reference needed,
    // bucket and distribution are in same stack
    this.distribution = new cloudfront.Distribution(
      this,
      'FrontendDistribution',
      {
        defaultBehavior: {
          origin: origins.S3BucketOrigin
            .withOriginAccessControl(
              this.frontendBucket
            ),
          viewerProtocolPolicy:
            cloudfront.ViewerProtocolPolicy
              .REDIRECT_TO_HTTPS,
          cachePolicy:
            cloudfront.CachePolicy.CACHING_OPTIMIZED,
        },
        defaultRootObject: 'index.html',
        errorResponses: [
          {
            httpStatus: 403,
            responseHttpStatus: 200,
            responsePagePath: '/index.html',
            ttl: cdk.Duration.seconds(0),
          },
          {
            httpStatus: 404,
            responseHttpStatus: 200,
            responsePagePath: '/index.html',
            ttl: cdk.Duration.seconds(0),
          },
        ],
      }
    );

    new cdk.CfnOutput(this, 'FrontendBucketName', {
      value: this.frontendBucket.bucketName,
      exportName: 'EquineFrontendBucketName',
    });

    new cdk.CfnOutput(this, 'DistributionUrl', {
      value: this.distribution
        .distributionDomainName,
      exportName: 'EquineDistributionUrl',
    });

    new cdk.CfnOutput(this, 'DistributionId', {
      value: this.distribution.distributionId,
      exportName: 'EquineDistributionId',
    });
  }
}
