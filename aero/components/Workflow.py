# Author: Ragy Haddad
import sys,os,logging
from aero.enums import JobStatus,DependancyStatus 
# Generic Workflow Interface
class GenericWorkflow:
    def __init__(self,name="generic-workflow",jobs=[],executor_status=0):
        self.name = name
        self.jobs = []
        self.executor_status = executor_status # 0 Not executed # 1 Running/inprogress # 2 Completed # 4 Error (stop workflow execution)
        self.logic = None
        self.current_job_index = 0
        self.current_job_dependancy = None # self.logic[self.current_job_index]
    
    # Check That all jobs within a workflow are unique
    def check_unique_job_names(self):
        names = {}
        for job in self.jobs:
            if job.name not in names:
                names[job.name] = 1 
            else:
                logging.error(" Job: %s name is not unique - Please make sure all job names are unique" % job.name)
                exit(1)


    # Check if a job depends on itself
    def check_self_dependance(self):
        for job in self.jobs:
            if job.name in job.depends_on:
                logging.error("Job: %s can not depend on itself" % job.name)
                exit(1)

    # Parse the current workflow and generate logic 
    def decode_logic(self):
        logic = {}
        job_names = [job.name for job in self.jobs]
        job_indicies = [i for i in range(len(self.jobs))]
        # Init Logic
        for idx in range(len(job_names)):
            logic[idx] = []
        for idx,job in enumerate(self.jobs):
            dependancy_list = job.depends_on
            if dependancy_list == None or len(dependancy_list) == 0:
                continue
            if isinstance(dependancy_list,list) == False:
                try:
                    dependancy_index = job_names.index(dependancy_list)
                except ValueError:
                    logging.error("Job Name %s does not exist in the workflow" % dependancy_list)
                    exit(1)
                logic[idx].append(dependancy_index)
            else:
                for dependancy in dependancy_list:
                    try:
                        dependancy_index = job_names.index(dependancy)
                    except ValueError:
                        logging.error("[Dependency Error] Job Name %s does not exist in the workflow" % dependancy)
                        sys.stdout.write("Your are trying to set a dependency that is not in the workflow\n")
                        exit(1)
                    logic[idx].append(dependancy_index)
        self.logic = logic
        return logic 
    
    # Initializes each job recieved by the workflow
    def set_jobs(self,jobs):
        for job in jobs:
            self.jobs.append(job)
        self.check_unique_job_names()
        self.check_self_dependance()
    
    # Serialize workflow to 
    #@TODO: works but Needs a rewrite - this is overwriting self this way  
    def serialize(self):
        serialized_jobs = []
        for idx,job in enumerate(self.jobs):
            self.jobs[idx] = self.jobs[idx].serialize() 
        serialized_workflow = self.__dict__ 
        return serialized_workflow
    # Check the workflow is valid 
    def validate_workflow(self):
        pass

    # Run Sequential Workflow
    def run_workflow_local(self):
        pass 

if __name__ == "__main__":
    pass

    


    
    



