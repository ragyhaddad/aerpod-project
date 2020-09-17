# Author: Ragy Haddad
import sys,os,json,time,logging
from kubernetes import client, config, utils, watch
from kubernetes.client.rest import ApiException 
import kubernetes.client 
from aero.monitors import LocalMonitor
from aero.enums import JobStatus
from datetime import datetime
# Execute Job Spec from a local machine on kubernetes
class JobExecutor:
    def __init__(self,verbose=False):
        config.load_kube_config()
        configuration = kubernetes.client.Configuration()
        self.api_instance = kubernetes.client.BatchV1Api(kubernetes.client.ApiClient(configuration))
        self.verbose = verbose 
        self.monitor = LocalMonitor()
        self.update_interval = 1 
    
    def wait_for_completion(self,job):
        while job.status != JobStatus.COMPLETED and job.status != JobStatus.FAILED:
            job.status = self.monitor.get_enumerated_job_status(job)
            if job.status == JobStatus.COMPLETED:
                stamp = str(datetime.now())
                logging.info("Job [%s] COMPLETED [%s]" % (job.name,stamp))
                return job
            elif job.status == JobStatus.FAILED:
                return job
            elif job.status == JobStatus.QUEUED or job.status == JobStatus.RUNNING or job.status == JobStatus.UNLAUNCHED:
                time.sleep(self.update_interval)
                self.wait_for_completion(job)
    """
    Execute Job 
        @job : Job
    """
    def execute_job(self,job,wait=False):
        # Dont execute running or failed jobs
        if job.status == JobStatus.RUNNING or job.status == JobStatus.FAILED:
            return job 
        try:
            if self.verbose:
                logging.info('Executing Job:%s' % job.name)
            api_response = self.api_instance.create_namespaced_job(job.body.metadata.namespace, job.body, pretty=True)
            # Once a job has a creation time_stamp then it is considered a RUNNING job 
            if api_response.metadata.creation_timestamp:
                job.status = JobStatus.RUNNING
                if wait:
                    stamp = str(datetime.now())
                    logging.info("Job [%s] RUNNING [%s]" % (job.name,stamp))
                    job = self.wait_for_completion(job)
                    
            return job
        except ApiException as e:
            body = json.loads(e.body)
            message = body['message']
            logging.info("Status: %i | Reason: %s | %s on cluster node" % (e.status,e.reason,message))
            job_status = self.monitor.get_enumerated_job_status(job) # Could remove this 2 lines in the future
            job.status = job_status
            return job
            

            
            
