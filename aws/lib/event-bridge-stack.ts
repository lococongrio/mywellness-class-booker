import * as cdk from "aws-cdk-lib";
import * as events from "aws-cdk-lib/aws-events";
import * as targets from "aws-cdk-lib/aws-events-targets";
import * as lambda from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";

interface MywellnessClassBookerEventBridgeStackProps extends cdk.StackProps {
  lambdaFunction: lambda.Function;
  env: Record<string, string | undefined>;
}

export class MywellnessClassBookerEventBridgeStack extends cdk.Stack {
  constructor(
    scope: Construct,
    id: string,
    props: MywellnessClassBookerEventBridgeStackProps,
  ) {
    super(scope, id, props);

    const rule = new events.Rule(this, "MywellnessClassBookerRule", {
      ruleName: "mywellness-class-booker-rule",
      // schedule: events.Schedule.expression('cron(59 5 ? * SUN-WED *)'), WINTER
      schedule: events.Schedule.expression("cron(59 4 ? * SUN-WED *)"), // SUMMER
    });

    rule.addTarget(new targets.LambdaFunction(props.lambdaFunction));
  }
}
