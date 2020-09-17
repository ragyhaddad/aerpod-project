# Author: Ragy Haddad
from kubernetes.client import models as k8s
class VolumeMount:
    def __init__(self,name,mount_path,read_only,sub_path=None):
        self.name = name
        self.mount_path = mount_path
        self.sub_path = sub_path
        self.read_only = read_only
        
    def to_k8s_volume_mount(self):
        return k8s.V1VolumeMount(mount_path=self.mount_path,sub_path=self.sub_path,name=self.name,read_only=self.read_only)

class Volume:
    def __init__(self,pv_name,pvc_name):
        self.pv_name = pv_name 
        self.pvc_name = pvc_name
    def to_k8s_volumes(self):
        return k8s.V1Volume(name=self.pv_name,persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name=self.pvc_name))