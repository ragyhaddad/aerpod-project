from aero.components import GenericJob,GenericWorkflow,GenericPipeline,Volume,VolumeMount
from aero.executors import LocalPipelineExecutor,JobExecutor


def single_workflow_test():
    job_a = GenericJob(name="job-a",image="alpine",cmds=["/bin/sh"],args=["-c","sleep 20"])
    job_b = GenericJob(name="job-b",image="alpine",cmds=["/bin/sh"],args=["-c","sleep 7"])
    job_c = GenericJob(name="job-c",image="alpine",cmds=["/bin/sh"],args=["-c","sleep 5"])
    job_d = GenericJob(name="job-d",image="alpine",cmds=["/bin/sh"],args=["-c","sleep 10"])

    job_b.add_dep(job_a)
    job_c.add_dep(job_b)
    job_d.add_dep([job_b,job_c])
    

    # Define Workflow
    workflow = GenericWorkflow()
    workflow.set_jobs([job_a,job_b,job_c,job_d])
    
    # Define Pipeline
    pipeline = GenericPipeline(name="hello-project")
    pipeline.set_workflow(workflow)
    pipeline_exec = LocalPipelineExecutor(update_interval=2)
    pipeline_exec.execute_pipeline(pipeline)

if __name__ == "__main__":
    single_workflow_test()
