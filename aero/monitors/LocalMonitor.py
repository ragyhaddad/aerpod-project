# Author: Ragy Haddad
import sys,os,logging
from kubernetes import client, config, utils, watch
from kubernetes.client.rest import ApiException 
import kubernetes.client 
from aero.enums import JobStatus

logging.getLogger().setLevel(logging.INFO)

# Use your own local machine as a workflow _ status
class LocalMonitor:
    def __init__(self,verbose=False):
        config.load_kube_config()
        configuration = kubernetes.client.Configuration()
        self.api_instance = kubernetes.client.BatchV1Api(kubernetes.client.ApiClient(configuration))
        self.namespace = "default"
        self.verbose = verbose
    
    # Check the status of a single job and return the enumerated status 
    def get_enumerated_job_status(self,job):
        try:
            response = self.api_instance.read_namespaced_job(name=job.name,namespace=job.namespace)
        except ApiException as e:
            if self.verbose:
                logging.error("Error retreiving job | either its unlaunched or queued: %s" % job.name)
            return job.status
        if response.status.active == 1 and response.status.succeeded == None and response.status.failed == None and response.status.start_time != None:
            job.status = JobStatus.RUNNING
        if response.status.succeeded == 1 and response.status.failed == None and response.status.active == None:
            job.status = JobStatus.COMPLETED
        if response.status.succeeded == None and response.status.failed != None and response.status.completion_time == None:
            job.status = JobStatus.FAILED
        return job.status
    
    # Get the body of a status
    def get_job_status(self,job_name):
        try:
            job = self.api_instance.read_namespaced_job(name=job_name,namespace=self.namespace)
        except ApiException as e:
            logging.error("Error retreiving job: %s" % job_name)
        return job.status 
    
    # Check an array of dependencies and return a signal
    # a dependency stage is satisfied when all the dependancy jobs are completed successfully 
    # if one job fails then the workflow fails 
    # if all jobs are running then we do nothing and wait for the next round  

    # Deprecated
    def get_dependancy_status(self,dependancy_job_names):
        status_list = []
        for job_name in dependancy_job_names:
            status = self.get_enumerated_job_status(job_name)
            status_list.append(status.value)
        if JobStatus.FAILED.value in status_list:
            return DependancyStatus.FAILED 
        elif JobStatus.NOTFOUND.value in status_list:
            return DependancyStatus.FAILED 
        elif JobStatus.RUNNING.value in status_list:
            return DependancyStatus.RUNNING 
        else:
            return DependancyStatus.COMPLETED

    # Checks Status for each job in worklfow and updates job accordingly
    # returns the updated workflow 
    def monitor_workflow(self,workflow):
        for job in workflow.jobs:
            if job.status != job.status.UNLAUNCHED and job.status != job.status.COMPLETED:
                job.status = self.get_enumerated_job_status(job)
        return workflow
    
    