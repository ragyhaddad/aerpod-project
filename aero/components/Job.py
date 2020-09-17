# Author: Ragy Haddad
import sys,os,yaml,json,logging
from kubernetes.client import models as k8s
from kubernetes import client,utils,config

from .Generator import JobGenerator
from aero.enums import JobStatus,DependancyStatus

logging.getLogger().setLevel(logging.INFO)
# GenericJob Interface
class GenericJob(JobGenerator):
    def __init__(self,status=None,dependency_status=None,deps_satisfied=False,**kwargs):
        super(GenericJob,self).__init__(**kwargs)
        self.depends_on = []
        self.deps_satisfied = False
        if dependency_status == None:
            self.dependency_status = DependancyStatus.UNLAUNCHED
        else:
            self.dependency_status = dependency_status 
        if status == None:
            self.status = JobStatus.UNLAUNCHED
        else:
            self.status = status 
        self.body = self.init_job()

    # Init shorter naming
    def init(self):
        self.init_job()
    
    def add_dep(self,dep_job):
        """ 
        Add a dependency or a list of dependencies 
        Args:
            dep_job: List(GenericJob) or GenericJob 
        Return:
            None 
        """
        if isinstance(dep_job,list) == False:
            self.depends_on.append(dep_job.name)
        else: 
            for dep in dep_job:
                self.depends_on.append(dep.name)
    def _create_from_yaml(self,path):
        """ 
        create a V1Job from a YAML file 
        uses k8s private function from source code.
        Args:
            path: String
        Return:
            k8s_V1Job
        """
        api_client = client.ApiClient()
        if os.path.exists(path):
            with open(path) as stream:
                pod = yaml.safe_load(stream)
        else:
            pod = yaml.safe_load(path)
        return api_client._ApiClient__deserialize_model(pod, k8s.V1Job)
    
    def init_from_yaml(self,path):
        """ 
        initialized job spec from a yaml file 
        and set the body spec to the yaml file
        Args:
            path: String
        Return:
            k8s_V1Job
        """
        self.body = self._create_from_yaml(path) 
        return self
    
    def serialize(self):
        serialized_body = self.body.to_dict()
        serialized = self.__dict__ 
        serialized["body"] = serialized_body
        # Serialize the Enums 
        serialized["dependency_status"] = serialized["dependency_status"].value 
        serialized["status"] = serialized["status"].value
        return serialized 

if __name__ == "__main__":
    pass
    

    
    


    



    





    












