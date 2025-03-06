import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';

export class MywellnessClassBookerLambdaStack extends cdk.Stack {
    public readonly lambdaFunction: lambda.Function;
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        const usernameSecret = secretsmanager.Secret.fromSecretNameV2(this, 'MyWellnessClassBookerUsernameSecret', 'mywellness-class-booker-username');
        const passwordSecret = secretsmanager.Secret.fromSecretNameV2(this, 'MyWellnessClassBookerPasswordSecret', 'mywellness-class-booker-password');

        const lambdaExecutionRole = new iam.Role(this, 'LambdaExecutionRole', {
            assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
        });

        usernameSecret.grantRead(lambdaExecutionRole);
        passwordSecret.grantRead(lambdaExecutionRole);

        const pythonLayer = new lambda.LayerVersion(this, 'MyWellnessClassBookerPythonLayer', {
            code: lambda.Code.fromAsset('/src/layer'),
            compatibleRuntimes: [lambda.Runtime.PYTHON_3_9],
            description: 'Layer with Python dependencies for MyWellnessClassBooker',
        });

        this.lambdaFunction = new lambda.Function(this, 'MyWellnessClassBooker', {
            runtime: cdk.aws_lambda.Runtime.PYTHON_3_9,
            handler: 'index.handler',
            code: lambda.Code.fromAsset('/src'),
            layers: [pythonLayer],
            environment: {
                HWF_USERNAME: usernameSecret.secretName,
                HWF_PASSWORD: passwordSecret.secretName,
            },
            timeout: cdk.Duration.seconds(60),
        });
    }
}