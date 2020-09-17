# Author: Ragy Haddad
from typing import * 
from kubernetes.client import models as k8s

class JobGenerator:
    def __init__(
        self,
        image: Optional[str] = None,
        name: Optional[str] = None,
        namespace: Optional[str] = 'default',
        volume_mounts: Optional[List[Union[k8s.V1VolumeMount, dict]]] = None,
        envs: Optional[Dict[str, str]] = None,
        cmds: Optional[List[str]] = None,
        args: Optional[List[str]] = None,
        labels: Optional[Dict[str, str]] = None,
        node_selectors: Optional[Dict[str, str]] = None,
        ports: Optional[List[Union[k8s.V1ContainerPort, dict]]] = None,
        volumes: Optional[List[Union[k8s.V1Volume, dict]]] = None,
        image_pull_policy: Optional[str] = None,
        restart_policy: Optional[str] = "Never",
        image_pull_secrets: Optional[str] = None,
        init_containers: Optional[List[k8s.V1Container]] = None,
        service_account_name: Optional[str] = None,
        resources: Optional[Union[k8s.V1ResourceRequirements, dict]] = None,
        annotations: Optional[Dict[str, str]] = None,
        affinity: Optional[dict] = None,
        hostnetwork: bool = False,
        tolerations: Optional[list] = None,
        security_context: Optional[Union[k8s.V1PodSecurityContext, dict]] = None,
        configmaps: Optional[List[str]] = None,
        dnspolicy: Optional[str] = None,
        schedulername: Optional[str] = None,
        pod: Optional[k8s.V1Pod] = None,
        pod_template_file: Optional[str] = None,
        priority_class_name: Optional[str] = None):

        self.name = name 
        self.namespace = namespace
        # Jobs
        self.job = k8s.V1Job()
        self.job.api_version = "batch/v1"
        self.job.kind = "Job"
        self.job.status = k8s.V1JobStatus() 
        # MetaData
        self.metadata = k8s.V1ObjectMeta()
        self.metadata.labels = labels
        self.metadata.name = name
        self.metadata.namespace = namespace
        self.metadata.annotations = annotations
        # Container
        self.container = k8s.V1Container(name='base')
        self.container.image = image
        self.container.env = []
        self.container.command = cmds or []
        self.container.args = args or []
        self.container.image_pull_policy = image_pull_policy
        self.container.ports = ports or []
        self.container.resources = resources
        self.container.volume_mounts = volume_mounts or []
        
        # Spec - Job spec config is a bit weird because you have to add a new template
        self.spec = k8s.V1PodSpec(containers=[self.container],restart_policy=restart_policy)
        self.template = k8s.V1PodTemplate()
        self.template.template = k8s.V1PodTemplateSpec()
        self.template.template.spec = self.spec
        # Volumes
        self.template.template.spec.volumes = volumes

        
    def init_job(self):
        """ 
        Initialize a job spec from object attributes
        and return the main spec
        """
        # Attach spec
        self.job.spec = k8s.V1JobSpec(template=self.template.template)
        self.job.metadata = self.metadata
        return self.job





