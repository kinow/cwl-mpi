# Ref: https://streamflow.di.unito.it/documentation/latest/cwl/cwl-runner.html
version: v1.0
workflows:
  workflow_name:
    type: cwl
    config:
      file: sr-workflow.cwl
      settings: sr-workflow-job.yml
    bindings:
      - step: /compile
        target:
          deployment: lumi_slurm
      - step: /run
        target:
          deployment: lumi_slurm
deployments:
  lumi_slurm:
    type: slurm
    workdir: /users/<USER>/cwl/cwl-mpi/examples/mpich-sr/streamflow/runs/
    config:
      hostname: lumi.csc.fi
      username: <USER>
      file: run-sr-mpirun-streamflow-slurm.jinja
      sshKey: ~/.ssh/id_rsa_mn
