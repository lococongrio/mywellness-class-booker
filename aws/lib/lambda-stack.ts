import * as cdk from "aws-cdk-lib";
import * as lambda from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs";

export class MywellnessClassBookerLambdaStack extends cdk.Stack {
  public readonly lambdaFunction: lambda.Function;
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const pythonLayer = new lambda.LayerVersion(
      this,
      "MyWellnessClassBookerPythonLayer",
      {
        code: lambda.Code.fromAsset("/src/layer"),
        compatibleRuntimes: [lambda.Runtime.PYTHON_3_9],
        description: "Layer with Python dependencies for MyWellnessClassBooker",
      },
    );

    this.lambdaFunction = new lambda.Function(this, "MyWellnessClassBooker", {
      runtime: cdk.aws_lambda.Runtime.PYTHON_3_9,
      handler: "index.handler",
      code: lambda.Code.fromAsset("/src"),
      layers: [pythonLayer],
      environment: {
        HWF_USERNAME: "HWF_USERNAME",
        HWF_PASSWORD: "HWF_PASSWORD",
      },
      timeout: cdk.Duration.seconds(60),
    });
  }
}
