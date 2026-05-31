# Ref: https://streamflow.di.unito.it/documentation/latest/cwl/cwl-runner.html
version: v1.0
workflows:
  workflow_name:
    type: cwl
    config:
      file: sr-workflow.cwl
      settings: sr-workflow-job.yml
      docker:
        - step: /
          deployment:
            type: singularity
            config: {}
