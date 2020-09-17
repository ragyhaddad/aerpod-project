# Author: Ragy Haddad
from aero.components import GenericWorkflow 
from components.Jobv2 import GenericJob
from aero.components import Volume,VolumeMount

class Mercury(GenericWorkflow):
    def __init__(self,name):
        super().__init__(name)
        self.mount_path = "/var"
        self.volume = Volume(pv_name="aero-nfs-volume",pvc_name="aero-nfs-claim").to_k8s_volumes()
        self.volume_mount = VolumeMount(name="aero-nfs-volume",mount_path=self.mount_path,read_only=False).to_k8s_volume_mount()
        self.pre_refbuilder_deps = []
    
    def init_A(self,sra_id):
        puller = GenericJob(
            name = sra_id + '-puller', 
            image = "gcr.io/dbtx-pipline/datapuller-aero",
            args = [], 
            volumes = [self.volume],
            volume_mounts = [self.volume_mount])
        trimmer = GenericJob(
            name = sra_id + '-trimmer', 
            image = "", 
            args = [], 
            volumes = [self.volume], 
            volume_mounts = [self.volume_mount])
        trimmer.add_dep(puller)
        assembler = GenericJob(
            name = sra_id + "-assembler", 
            image = "",
            args = [],
            volumes = [self.volume],
            volume_mounts = [self.volume_mount])
        assembler.add_dep(trimmer) 
        bgccaller = GenericJob(
            name = sra_id + '-bgccaller',
            image = "", 
            args = [],
            volumes = [self.volume], 
            volume_mounts = [self.volume_mount])
        bgccaller.add_dep(assembler) 
        # Jobs required for bgccaller
        self.pre_refbuilder_deps.append(bgccaller)
        # Add Stage 1 Jobs to workflow
        self.jobs.extend([puller,trimmer,assembler,bgccaller])
    def init_B(self,pre_refbuilder_deps):
        refbuilder = GenericJob(
            name = self.name + "-refbuilder",
            image = "",
            args = [], 
            volumes = [self.volume], 
            volume_mounts = [self.volume_mount]
        )
        refbuilder.add_dep(pre_refbuilder_deps)
        self.jobs.append(refbuilder)
    def init_jobs(self,sra_list):
        # Init A
        for sra in sra_list:
            self.init_A(sra)
        # Init B 
        self.init_B(self.pre_refbuilder_deps)
        


        
m = Mercury(name='nash-1')
m.init_jobs(["SRX1","SRX2"])
for job in m.jobs:
    print(job.name)
    print(job.depends_on)
    
    



        