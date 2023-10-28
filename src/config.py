import os as __os

__env = 'dev'
__aws_region = __os.getenv('CDK_DEFAULT_REGION')
__account_number = __os.getenv('CDK_DEFAULT_ACCOUNT')
dev = {
    "healthCheck_queue_url": "https://sqs.{}.amazonaws.com/{}/{}-{}-{}-healthCheckQueue".format(
        __aws_region, __account_number, __env, __aws_region, __account_number)
}
