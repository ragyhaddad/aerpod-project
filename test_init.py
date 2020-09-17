from aero.components.Jobv2 import GenericJob 
from aero.executors import JobExecutor 

job = GenericJob(
    name = 'hello-job',
    image = 'alpine',
    cmds = ["/bin/sh"],
    args = ["-c","echo helloworld!"],
)
print(job.body.metadata.namespace)

executor = JobExecutor()
executor.execute_job(job,wait=True)