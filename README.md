### Aeropod HPC Framework
Lightweight kubernetes workflow orchestrator 

##### Description:
Aeropod is a python framework that allows you to progrommatically define complex workflows in a simple flexible way. It can run on any environment that has kubectl configured with a context. 

##### Why use this?
The reason this was developed was for running quick workflows that run to completetion using exclusively python without having to edit YAML files or set up deployments, the goal is minimalism and simplicity. Two amazing frameworks that do a similar task are Argo and Apache Airflow. However, this was designed to only orchestrate kubernetes jobs which makes it more lightweight and simple. The framework is mainly inspired by life sciences data pipelines. 

### Dependencies 
    python>=3.6
### Install with pip  
    git clone https://github.com/deepbiome/aeropod-project.git 
    cd aeropod-project
    pip install .  

### Install with conda 
    git clone https://github.com/deepbiome/aeropod-project
    conda create --name aero-env python=3.7
    cd aeropod-project
    conda activate aero-env
    pip install .

##### Configure kubectl
if your kubectl is already configured skip this section. if you want to test this code with a local cluster set up a minikube cluster from here [Minikube Installation](https://kubernetes.io/docs/tasks/tools/install-minikube/) aero will run the workflows specified on your kubectls current context.

#### Example Job:
``` python
from aero.components import GenericJob 
from aero.executors import JobExecutor 

job = GenericJob(
    name = 'hello-job',
    image = 'alpine',
    cmds = ["/bin/sh"],
    args = ["-c","echo helloworld!"]
)

executor = JobExecutor()
executor.execute_job(job,wait=True)
```
The GenericJob class allows you to create the equivalent of a V1/Job on kubernetes, it uses the kubernetes python client to configure the jobs requested. The Job class is not designed to run webservers or APIs. The GenericJob is a containerized process that runs to completion.  
#### Example Simple Workflow:
Running a simple workflow with dependencies
``` python
from aero.components import GenericJob,GenericWorkflow,GenericPipeline,Volume,VolumeMount
from aero.executors import LocalPipelineExecutor,JobExecutor
def single_workflow_test():
    job_a = GenericJob(name="job-a",image="alpine",cmds=["/bin/sh"],args=["-c","sleep 20"])
    job_b = GenericJob(name="job-b",image="alpine",cmds=["/bin/sh"],args=["-c","sleep 7"])
    job_c = GenericJob(name="job-c",image="alpine",cmds=["/bin/sh"],args=["-c","sleep 5"])
    job_d = GenericJob(name="job-d",image="alpine",cmds=["/bin/sh"],args=["-c","sleep 10"])

    job_b.add_dep(job_a)
    job_c.add_dep(job_a)
    job_d.add_dep([job_b,job_c])
    
    # Define Workflow
    workflow = GenericWorkflow()
    workflow.set_jobs([job_a,job_b,job_c,job_d])

    # Define Pipeline
    pipeline = GenericPipeline(name="hello-project")
    pipeline.set_workflow(workflow)
    # Execute
    pipeline_exec = LocalPipelineExecutor()
    pipeline_exec.execute_pipeline(pipeline)

if __name__ == "__main__":
    single_workflow_test()
```
#### Example Advanced Workflow: 
``` python 
from aero.components import GenericJob,GenericWorkflow 
"""
    Construct a Diamond DAG workflow
    When constructing dags we inherit the Generic Workflow class 
    and set the jobs of the workflow accordingly 
"""
class DiamondDAG(GenericWorkflow):
    def __init__(self): # Must specify name on init
        super().__init__()
        self.mount_path = "/var/"
    # Init Jobs and DAG
    def init_jobs(self):
        job_a = GenericJob(
            name = "job-a",
            image = "alpine",
            cmds = ["/bin/sh"],
            args = ["-c","echo hello from job-a; sleep 3"])
        job_b = GenericJob(
            name = "job-b",
            image = "alpine",
            cmds = ["/bin/sh"],
            args = ["-c","echo hello from job-b; sleep 4"])
        job_b.add_dep(job_a)
        job_c = GenericJob(
            name = "job-c",
            image = "alpine",
            cmds = ["/bin/sh"],
            args = ["-c","echo hello from job-c; sleep 5"])
        job_c.add_dep(job_b)
        job_d = GenericJob(
            name = "job-d",
            image = "alpine",
            cmds = ["/bin/sh"],
            args = ["-c","echo hello from job-d; sleep 5"]) 
        job_d.add_dep([job_b,job_c])
        # Add to GenericWorkflow Attributes
        self.jobs.extend([job_a,job_b,job_c,job_d])
        return self
```
##### Running The Workflow
``` python
from aero.components import GenericPipeline 
from aero.executors import LocalPipelineExecutor
# Init Workflow
myworkflow = DiamondDAG() # Created above 
myworkflow.init_jobs()
# Init Pipeline
pipeline  = GenericPipeline('diamond-1')
pipeline.set_workflow(myworkflow) # Initialize the pipeline with the given workflow
# Init Executor
executor = LocalPipelineExecutor()
executor.execute_pipeline(pipeline)
```

##### Clean up 
``` aero-cli delete <pipeline_name> ``` (In Progress) 

### Guides:
* [Getting Started](https://github.com/deepbiome/aeropod-project/wiki/Getting-Started)
* [Run a Workflow and Monitor Progress](https://github.com/deepbiome/aeropod-project/wiki/Creating-a-workflow-and-running-it)
* [Bioinformatics Workflow Example](https://github.com/deepbiome/aeropod-project/wiki/Bioinformatics-Workflow-Example)
* [Configuring Persistent Volumes]() [In Progress]









