# Ref: https://streamflow.di.unito.it/documentation/latest/cwl/cwl-runner.html
version: v1.0
workflows:
  workflow_name:
    type: cwl
    config:
      file: run-sr-mpireq-nodocker.cwl
      settings: run-sr-mpireq-nodocker-streamflow-job.cwl
