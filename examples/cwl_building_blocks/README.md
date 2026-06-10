# CWL Building Blocks

In the folder `./images`, there is an image that shows the CWL building blocks.
These are tools and workflows (well, not all blocks, but we were aiming at
conciseness) that call `cat` and `grep.

This folder contains the CWL workflows that represent that example.

`cat` is used to print a file with a poem in it[^1]. `grep`
then searches for the word "terra" (searching for land…).

The output of running the workflow is saved here for reference. See
files `cat.log` and `grep.log`. The `grep_tool.cwl` is intentionally
named with the `_tool` suffix to make it clear that CWL files can have
any name, not necessarily the name of the executable.

```bash
$ cwltool workflow.cwl job.yml
```

[^1]: Adiós ríos, adiós fontes, by Rosalía de Castro,
published over 100 years ago (public domain),
https://rosalia.gal/planeta-rosalia/adios-rios-ao-espanol/
