broker_url = 'pyamqp://'
backend = 'rpc://'
timezone = 'Europe/London'
enable_utc = True
beat_schedule = {
    'add-every-5-seconds':{
         'task':'bbc.bbc_task.apply_async(queue="bbc")',
         'schedule':60*2.0,
     },
}

task_routes = {
        'bbc_task':{
              'queue': 'bbc',
              'routing_key': 'bbc.compress',
                },
}

