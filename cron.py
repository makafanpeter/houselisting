from datetime import datetime
from urlparse import urlparse
import os
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from crawler import crawl, format_address
import signal

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
url = urlparse(redis_url)
job_stores = {
    'default': RedisJobStore(host=url.hostname, port=url.port, password=url.password)
}

scheduler = BackgroundScheduler(jobstores=job_stores)

job1 = scheduler.add_job(crawl, 'cron', day_of_week='mon-sun', hour=23, id='crawler_cron', replace_existing=True)

job2 = scheduler.add_job(format_address, 'cron', day_of_week='mon-sun', hour=13, id='address_formatter_cron',
                         replace_existing=True, next_run_time=datetime.now())

scheduler.start()

scheduler.print_jobs()


signal.pause()
