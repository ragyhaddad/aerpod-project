# Author: Ragy Haddad
import sys,os
import logging 
# Generic Pipeline Interface 
class GenericPipeline:
    def __init__(self,name='generic-pipeline',workflows = None):
        self.name = name
        self.workflows = []
        self.completed = 0 
        self.successful = 0 
        self.running = 0 
        self.namespace = "default"
        self.n_jobs = 0 
        self.last_update = None
    # Attach workflow to pipeline and decode workflow logic
    def set_workflow(self,wfs):
        print('-- Setting workflow')
        if isinstance(wfs,list):
            for wf in workflows:
                if len(wf.jobs) == 0:
                    logging.error("Error workflow [%s] has no jobs initialized" % wf.name)
                    exit(1)
                self.workflows.append(wf)
        else:
            if len(wfs.jobs) == 0:
                logging.error("Error workflow [%s] has no jobs initialized" % wfs.name)
                exit(1)
            else:
                self.workflows.append(wfs)
        # Decode Logic
        self.decode_all_workflow_logic()
    
    # Parse Each Workflow logic and set the logicvalues on the workflowss
    def decode_all_workflow_logic(self):
        for idx,workflow in enumerate(self.workflows):
            self.workflows[idx].logic = self.workflows[idx].decode_logic()
        return 0 
    # Convert a pipeline to a JSON list of commands
    def serialize(self):
        for idx,workflow in enumerate(self.workflows):
            self.workflows[idx] = self.workflows[idx].serialize()
        serialized_pipeline = self.__dict__ 
        return serialized_pipeline

if __name__ == "__main__":
    pass

