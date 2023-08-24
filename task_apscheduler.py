import functools
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import AndTrigger, OrTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

# This decorator can be applied to any job function to log the elapsed time of each job
def print_elapsed_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_timestamp = time.time()
        print('LOG: Running job "%s"' % func.__name__)
        result = func(*args, **kwargs)
        print('LOG: Job "%s" completed in %d seconds' % (func.__name__, time.time() - start_timestamp))
        return result

    return wrapper

# this decorator can be applied to any job function to catch any exceptions that may be raised during the job
def catch_exceptions():
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                print(traceback.format_exc())
        return wrapper
    return catch_exceptions_decorator

@print_elapsed_time
@catch_exceptions()
def job(param1, param2):
    print(f"param1: {param1}, param2: {param2}")
    # print(1/0)

if __name__ == "__main__":
    # Simple example of a job that runs every 2 seconds
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', seconds=2, args=['hello', 'world'], id='my_job_id')
    scheduler.start()
    
    # customer trigger run every 2 hours, but only on Saturdays and Sundays
    # custom_trigger = AndTrigger([
    #         IntervalTrigger(hours=2),
    #         CronTrigger(day_of_week='sat,sun')
    #     ])
    
    # custom trigger run every Monday at 2am and every Tuesday at 3pm
    # custom_trigger = OrTrigger([
    #     CronTrigger(day_of_week='mon', hour=2),
    #     CronTrigger(day_of_week='tue', hour=15)
    # ])
    
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(job, custom_trigger, args=['param1', 'param2'], id='my_job_id')
    # scheduler.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Shutdown")
        scheduler.remove_job('my_job_id')
        scheduler.shutdown()