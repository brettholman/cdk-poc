import os as __os

__env = 'dev'
__aws_region = __os.getenv('CDK_DEFAULT_REGION')
__account_number = __os.getenv('CDK_DEFAULT_ACCOUNT')
dev = dict(
    sqs_name="{}-{}-{}-healthCheckQueue".format(
        __env, __aws_region, __account_number)
)
