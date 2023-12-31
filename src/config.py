import os as __os
resources = dict([
    ("health_check_queue_url",
        __os.getenv("health_check_queue_url")
     ),
    ("health_check_dynamo_table",
        __os.getenv("health_check_dynamo_table")
     ),
    ("health_check_sns_topic",
        __os.getenv("health_check_sns_topic")
     ),
    ("health_check_s3_bucket",
        __os.getenv("health_check_s3_bucket")
     )
])
