from aws_cdk import (
    Duration,
    Stack,
    RemovalPolicy,
    aws_sqs as sqs,
    aws_dynamodb as dynamo,
    aws_lambda as lambda_,
    aws_sns as sns,
    aws_iam as iam
)
from constructs import Construct


class HealthCheckStack(Stack):

    def __create_name(self, unique_name, env="dev") -> str:
        return "{}-{}-{}-{}".format(
            env, self.region, self.account, unique_name)

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        health_check_queue = sqs.Queue(
            self,
            "health_check_queue",
            visibility_timeout=Duration.seconds(300),
            queue_name=self.__create_name("healthCheckQueue")
        )

        sqs_policy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["sqs:sendMessage"],
                    resources=[health_check_queue.queue_arn]
                )
            ]
        )

        health_check_table = dynamo.Table(
            self,
            "health_table",
            table_name=self.__create_name("healthCheckTable"),
            partition_key=dynamo.Attribute(
                name="pk",
                type=dynamo.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY
        )

        dynamo_policy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["dynamodb:Get*"],
                    resources=[health_check_table.table_arn]
                )
            ]
        )

        health_check_sns_topic = sns.Topic(
            self,
            "health_sns_topic",
            topic_name=self.__create_name("healthCheckSnsTopic")
        )

        sns_policy = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["sns:Publish"],
                    resources=[health_check_sns_topic.topic_arn]
                )
            ]
        )

        lambda_execution_role = iam.Role(
            self,
            "lambda_execution_role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            inline_policies={
                "dynamo_read": dynamo_policy,
                "sqs_send_message": sqs_policy,
                "sns_publish": sns_policy
            }
        )

        lambda_.Function(
            self,
            "healthCheckLambda",
            function_name="healthCheckLambda",
            code=lambda_.Code.from_asset("src"),
            handler="handlers.healthCheckLambda.handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            environment={
                "health_check_queue_url": health_check_queue.queue_url,
                "health_check_dynamo_table": health_check_table.table_name,
                "health_check_sns_topic": health_check_sns_topic.topic_arn
            },
            role=lambda_execution_role)
