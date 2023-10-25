import aws_cdk as core
import aws_cdk.assertions as assertions

from health_check.health_check_stack import HealthCheckStack

# example tests. To run these tests, uncomment this file along with the example
# resource in health_check/health_check_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = HealthCheckStack(app, "health-check")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
