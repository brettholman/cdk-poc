from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
    aws_dynamodb as dynamo,
    aws_lambda as lambda_,
    aws_iam as iam,
    CfnOutput
)
from constructs import Construct


class HealthCheckStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        health_check_queue = sqs.Queue(
            self, "HealthCheckQueue",
            visibility_timeout=Duration.seconds(300),
            queue_name="dev-{}-{}-healthCheckQueue".format(
                self.region, self.account)
        )

        health_check_table = dynamo.Table(
            self,
            "healthTable",
            partition_key=dynamo.Attribute(
                name="pk", type=dynamo.AttributeType.STRING)
        )

        fn_health_check = lambda_.Function(self, "healthCheckLambda",
                                           function_name="healthCheckLambda",
                                           code=lambda_.Code.from_asset(
                                               "src"),
                                           handler="handlers.healthCheckLambda.handler",
                                           runtime=lambda_.Runtime.PYTHON_3_9,
                                           environment={
                                               "health_check_queue_url": health_check_queue.queue_url
                                           })

        CfnOutput(self, "queue", value="name={} url={}".format(
            health_check_queue.queue_name, health_check_queue.queue_url))
