# Author: Ragy Haddad
from aero.components import GenericPipeline
from aero.executors import LocalPipelineExecutor  
from aero.workflow_templates.diamond import DiamondDAG

def main():
    workflow = DiamondDAG()
    workflow.init_jobs() 
    pipeline = GenericPipeline(name="diamond-pipeline")
    pipeline.set_workflow(workflow)
    exc = LocalPipelineExecutor()
    exc.execute_pipeline(pipeline)
if __name__ == "__main__":
    main()