from aero.components import GenericJob,GenericWorkflow 

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