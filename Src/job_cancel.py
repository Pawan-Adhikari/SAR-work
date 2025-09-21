import asf_search as asf
import hyp3_sdk

# Authenticate using environment variables
hyp3 = hyp3_sdk.HyP3(username='pon.adk', password='qeDriz-juhdu3-feckav')



# Let's say we want to cancel the first one in the list

# Pass a single job object
print(hyp3.check_credits())

# Alternatively, you can pass a list of job IDs
# job_id_to_cancel = 'your_job_id_here'
# cancelled_jobs = hyp3.cancel_jobs([job_id_to_cancel])