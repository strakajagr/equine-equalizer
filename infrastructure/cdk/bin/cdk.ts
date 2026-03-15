#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib/core';
import { StorageStack } from '../lib/storage-stack';
import { DatabaseStack } from '../lib/database-stack';
import { ComputeStack } from '../lib/compute-stack';
import { FrontendStack } from '../lib/frontend-stack';

const app = new cdk.App();

const env = {
  account: process.env.CDK_DEFAULT_ACCOUNT,
  region: process.env.CDK_DEFAULT_REGION,
};

// 1. StorageStack — S3 buckets (no dependencies)
const storage = new StorageStack(app, 'EquineStorageStack', { env });

// 2. DatabaseStack — VPC + Aurora Serverless (no dependencies)
const database = new DatabaseStack(app, 'EquineDatabaseStack', { env });

// 3. ComputeStack — Lambdas, EventBridge, API Gateway (depends on Storage + Database)
const compute = new ComputeStack(app, 'EquineComputeStack', {
  env,
  vpc: database.vpc,
  lambdaSecurityGroup: database.lambdaSecurityGroup,
  dbCluster: database.cluster,
  rawDataBucket: storage.rawDataBucket,
  processedDataBucket: storage.processedDataBucket,
  modelArtifactsBucket: storage.modelArtifactsBucket,
});
compute.addDependency(storage);
compute.addDependency(database);

// 4. FrontendStack — CloudFront distribution (depends on Storage)
const frontend = new FrontendStack(app, 'EquineFrontendStack', {
  env,
  frontendBucket: storage.frontendBucket,
});
frontend.addDependency(storage);

app.synth();
