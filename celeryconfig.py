broker_url = 'pyamqp://'
backend = 'rpc://'
timezone = 'Europe/London'
enable_utc = True
beat_schedule = {
    'add-every-5-seconds':{
         'task':'bbc.bbc_task',
         'schedule':60*2.0,
     },
}

