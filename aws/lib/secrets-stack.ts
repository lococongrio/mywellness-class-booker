import * as cdk from 'aws-cdk-lib';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { Construct } from 'constructs';

export class MywellnessClassBookerSecretsStack extends cdk.Stack {
  public readonly mywellnessClassBookerUsernameSecret: secretsmanager.Secret;
  public readonly mywellnessClassBookerPasswordSecret: secretsmanager.Secret;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    this.mywellnessClassBookerUsernameSecret = new secretsmanager.Secret(this, 'MywellnessClassBookerUsernameSecret', {
      secretName: 'mywellness-class-booker-username',
    });
    this.mywellnessClassBookerPasswordSecret = new secretsmanager.Secret(this, 'MywellnessClassBookerPasswordSecret', {
      secretName: 'mywellness-class-booker-password',
    });
  }
}