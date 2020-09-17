# Author: Ragy Haddad
import sys,os,json 
import datetime,time,logging
from typing import List
from datetime import datetime 

from aero.components import GenericJob
from aero.loggers import ProgressLogger 
from aero.monitors import LocalMonitor
from aero.executors import JobExecutor
from aero.enums import JobStatus,DependancyStatus

"""
    A pipeline event is one full itteration over a pipeline spec
"""
class LocalPipelineEvent:
    def __init__(self,pipeline,verbose=True):
        self.pipeline = pipeline 
        self.name = self.pipeline.name
        self.pipeline_progress = None # Loads Database Progress to Keep track of the last Job
        self.monitor = LocalMonitor()
        self.executor = JobExecutor(verbose=verbose) 
        self.logger = ProgressLogger()
        self.verbose = verbose
    # Skip logic execution on a job if its dependency is pending
    def dependency_not_executed(self,pending_jobs_index_list,dependancy_index_list):
        dep_not_executed = False
        for i in dependancy_index_list:
            for j in pending_jobs_index_list:
                if i == j:
                    dep_not_executed = True 
        return dep_not_executed 

    def get_job_dependancy_status(self,jobs:List[GenericJob]) -> DependancyStatus:
        """
        Get status of each job in a list of jobs with type Generic Job
        Args:
            list(GenericJob): a list of Generic Jobs  
        Returns:
            DependancyStatus
        """
        status_list = []
        for job in jobs:
            status = job.status.value 
            status_list.append(status)
        if len(status_list) == 0:
            return DependancyStatus.INDEPENDANT
        else:
            if list(set(status_list))[0] == JobStatus.COMPLETED.value:
                return DependancyStatus.COMPLETED
            elif JobStatus.FAILED.value in status_list:
                return DependancyStatus.FAILED 
            elif JobStatus.NOTFOUND.value in status_list:
                return DependancyStatus.UNLAUNCHED
            elif JobStatus.RUNNING.value in status_list:
                return DependancyStatus.RUNNING 
            elif JobStatus.QUEUED.value in status_list:
                return DependancyStatus.RUNNING
            elif JobStatus.UNLAUNCHED in status_list:
                return DependancyStatus.RUNNING

    def handle_job_dependancy_status(self,job,dependancy_status):
        """ 
        According to the status of jobs needed for another job
        return the global status of all dependencies for a given job 
        Args:
            job (GenericJob): a job to query 
            dependency_status (DependencyStatus) : the global status of dependency jobs
        Return:
            job (GenericJob)
        """
        t_stamp = str(datetime.now())
        if dependancy_status == DependancyStatus.INDEPENDANT and job.status != JobStatus.COMPLETED:
            job.deps_satisfied = True
        elif dependancy_status == DependancyStatus.RUNNING:
            if self.verbose:
                logging.info("RUNNING JOB %s [%s]" % (job.name,t_stamp))
            job.status = JobStatus.QUEUED
            job.deps_satisfied = False
            if self.verbose:
                logging.info("QUEUING JOB %s [%s]" % (job.name,t_stamp))
        elif dependancy_status == DependancyStatus.FAILED:
            if self.verbose:
                logging.error("One or more Jobs in the workflow failed")
            job.deps_satisfied = False
        elif dependancy_status == DependancyStatus.COMPLETED:
            if self.verbose:
                logging.info("Job %s COMPLETED [%s]" % (job.name,t_stamp))
            job.deps_satisfied = True
        return job
    
    def update_pipeline(self) -> None:
        """
        update the pipeline spec, execute all steps needed to update current states 
        if states are satisfied run the queued jobs, and update the status 
        """
        for workflow in self.pipeline.workflows:
            updated_workflow = self.monitor.monitor_workflow(workflow)
            for job_index,job in enumerate(updated_workflow.jobs):
                self.logger.write_current_state(self.pipeline)
                dependancy_list = workflow.logic[int(job_index)]
                dependancy_jobs =[workflow.jobs[idx] for idx,j in zip(dependancy_list,workflow.jobs)]
                dependancy_status = self.get_job_dependancy_status(dependancy_jobs)
                job = self.handle_job_dependancy_status(job,dependancy_status)
                if job.deps_satisfied and job.status != JobStatus.COMPLETED:
                    job = self.executor.execute_job(job)
                workflow_global_status = [j.status for j in workflow.jobs]
                # print(workflow_global_status)
                if workflow_global_status != None:
                    workflow_global_status = list(set(workflow_global_status))
                    workflow_global_status = [s.value for s in workflow_global_status ]
                    if len(workflow_global_status) == 1 and workflow_global_status[0] == 2:
                        if workflow_global_status[0] == JobStatus.COMPLETED.value:
                            logging.info('All Jobs COMPLETED')
                            exit()
                            
        
    
