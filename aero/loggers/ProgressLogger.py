# Author: Ragy Haddad
import sys,os,json,logging
import glob
from datetime import datetime
from tinydb import TinyDB, Query

class ProgressLogger:
    def __init__(self):
        self.data_path = '/tmp/aero-database'
        if os.path.isdir(self.data_path) == False:
            os.system("mkdir %s" % self.data_path)
    # Init Pipeline
    def init_pipeline(self,pipeline):
        database_path = os.path.join(self.data_path,pipeline.name + '.json')  
        db = TinyDB(database_path)
        pipeline_init_progress = self.pipeline_progress_interface(pipeline)
        db.insert(pipeline_init_progress)
    # Update Database state
    def write_current_state(self,pipeline):
        database_path = os.path.join(self.data_path,pipeline.name + '.json')  
        if os.path.isfile(database_path) == False:
            self.init_pipeline(pipeline)
        else:
            db = TinyDB(database_path)
            current_state = self.pipeline_progress_interface(pipeline)
            db.update(current_state)
    # Check if a pipeline exists
    def check_pipeline_exists(self,pipeline_name):
        available_pipelines = [f.split(".")[0] for f in glob.glob(self.data_path + "/*.json")]
        available_pipelines = [os.path.basename(f) for f in available_pipelines]
        if pipeline_name not in available_pipelines:
            logging.error("Pipeline [%s] Does not exist" % pipeline_name)
            print('Source:')
            print(self.data_path)
            sys.stdout.write('Available Pipelines:\n')
            sys.stdout.write('--------------------\n')
            for p in available_pipelines:
                sys.stdout.write("%s\n" % p)
            return False 
        else:
            return True
    # Get current State from database
    def get_current_state(self,pipeline_name):
        database_path = os.path.join(self.data_path,pipeline_name + '.json')
        db = TinyDB(database_path)
        if len(db.all()) == 0:
            logging.error("Error Opening Pipeline database. It seems empty")
            exit(1) 
        current_state = db.all()[0]
        return current_state 
    # From a pipeline job extract progress specific info 
    def pipeline_progress_interface(self,pipeline):
        p_ = {}
        pipeline_name = pipeline.name
        workflows = pipeline.workflows 
        time_stamp = datetime.now()
        time_stamp = time_stamp.strftime("%c")
        p_["name"] = pipeline.name
        p_["succeeded"] = 0
        p_["failed"] = 0
        p_["running"] = 0
        p_["workflows"] = {}
        p_["last_updated"] = str(time_stamp)
        for wf in workflows:
            wf_ = {}
            wf_["name"] = wf.name 
            wf_["jobs"] = {}
            wf_["n_jobs"] = len(wf.jobs)
            wf_["logic"] = wf.logic
            for job in wf.jobs:
                j_ = {}
                j_["name"] = job.name 
                j_["status"] = job.status.value 
                j_["spec"] = None
                j_["depends_on"] = job.depends_on
                wf_["jobs"][job.name] = j_ 
            p_["workflows"][wf.name] = wf_
        return p_ 
                  




