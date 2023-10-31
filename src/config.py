import os as __os
resources = dict([
    ("health_check_queue_url",
        __os.getenv("health_check_queue_url")
     ),
    ("health_check_dynamo_table",
        __os.getenv("health_check_dynamo_table")
     )
])
