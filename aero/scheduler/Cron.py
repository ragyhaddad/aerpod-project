# Author: Ragy Haddad
import os 
import dill 
import logging
import time
from datetime import datetime
from aero.executors import LocalPipelineExecutor   
class CronScheduler:
    def __init__(self,verbose=False):
        self.time_frame = 5 # Update Pipeline every 5 seconds for dev 
        self.sessions_path = '/tmp/aero-sessions/' # Add absolute path 
        self.verbose = verbose 
        if os.path.isdir(self.sessions_path) == False:
            os.system("mkdir %s" % self.sessions_path)
    # Save dill pipeline session object - this function will overwrite the current pipeline
    def init_pipeline_session(self,pipeline):
        pipeline_name = pipeline.name 
        session_fpath = os.path.join(self.sessions_path,pipeline_name + ".dl")
        if os.path.isfile(session_fpath):
            if self.verbose:
                logging.warning("Pipeline [%s] already exists in sessions. Overwriting sessions is disable" % pipeline_name)
                logging.error("Pipeline not scheduled")
            return False 
        else:
            # Initialize a new session 
            with open(session_fpath,"wb") as f:
                dill.dump(pipeline,f)
    # Get pipeline current session 
    def get_pipeline_session(self,pipeline_name):
        session_path = os.path.join(self.sessions_path,pipeline_name + ".dl")
        pipeline = None 
        with open(session_path,"rb") as f:
            pipeline = dill.load(f)
        return pipeline 
    # 
    def init_pipeline_schedule(self,pipeline):
        new_session = self.init_pipeline_session(pipeline)
        pipeline_session_path = os.path.join(self.sessions_path,pipeline.name + ".dl")

         

            


    
        
        
        



