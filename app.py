#!/usr/bin/env python3
import os

import aws_cdk as cdk

from health_check.health_check_stack import HealthCheckStack


app = cdk.App()
HealthCheckStack(app, "HealthCheckStack",
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
)

app.synth()
