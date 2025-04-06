#!/usr/bin/env node
import { App, Tags } from "aws-cdk-lib";
import { StackConfiguration } from "../lib/stack-configuration";
import { MywellnessClassBookerLambdaStack } from "../lib/lambda-stack";
import { MywellnessClassBookerEventBridgeStack } from "../lib/event-bridge-stack";

const app = new App();
Tags.of(app).add("application", StackConfiguration.getServiceName());

const env = {
  account: process.env.CDK_DEFAULT_ACCOUNT,
  region: process.env.CDK_DEFAULT_REGION,
};

const lambdaStack = new MywellnessClassBookerLambdaStack(
  app,
  "MywellnessClassBookerLambdaStack",
  {
    env,
  },
);
new MywellnessClassBookerEventBridgeStack(
  app,
  "MywellnessClassBookerEventBridgeStack",
  {
    lambdaFunction: lambdaStack.lambdaFunction,
    env,
  },
);
