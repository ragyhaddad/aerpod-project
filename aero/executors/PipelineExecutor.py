# Author: Ragy Haddad
import sys,os,time
from aero.events import LocalPipelineEvent 

class LocalPipelineExecutor:
    def __init__(self,update_interval=1):
        self.pipeline = None
        self.update_interval = update_interval
    def execute_pipeline(self,pipeline):
        self.pipeline_event = LocalPipelineEvent(pipeline)
        while True:
            status = self.pipeline_event.update_pipeline()
            if status == 0:
                exit()
            time.sleep(self.update_interval)
            
            
            
