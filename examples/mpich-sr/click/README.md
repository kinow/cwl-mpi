# Testing cwl2click

This folder contains an extra test for the example of `sr.c` with CWL and MPI.

We test TerraDue's utility `cwl2click`[^1]. It reads a CWL workflow and produces a
Python click script. Through the click library, the generated script parses the
command line input accepting it to run the workflow in a similar way to what cwltool
does.

For example, from the parent directory you can test it with this command:

```bash
$ cwl2click --output ./ ../sr-workflow.cwl
```

[^1]: https://terradue.github.io/cwl2click/execution/
