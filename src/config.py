import os as __os
resources = dict([
    ("health_check_queue_url",
        __os.getenv("health_check_queue_url")
     )
])
