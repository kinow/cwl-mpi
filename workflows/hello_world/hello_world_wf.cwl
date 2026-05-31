cwlVersion: v1.2
class: Workflow

inputs:
  message:
    type: string
    default: "Hello World"

outputs: []

steps:
  echo_step:
    run: hello_world.cwl
    in:
      message: message
    out: []

