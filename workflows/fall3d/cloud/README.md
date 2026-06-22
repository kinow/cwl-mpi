# Cloud Environments

These automation scripts were used to create the cloud environment on Hetzner Cloud.
This is a small, simple, two-node cluster.

- `./hetzner/`: Scripts used for running the FALL3D Workflow, that runs FALL3D
Etna example workflow from GET-IT consortium, developed by GEO3BCN. 

Start by running `base.sh` on both master and worker nodes.

Then, run `master.sh` on the master node, and `worker.sh` on the worker node.

Look at the output of `master`, and follow the instructions to finish the setup.

Remember to export these variables in the master node, so MPI correctly starts
run this on both nodes.

```bash
cwlmpi@master:/shared$ cat > ~/.pmix/mca-params.conf <<EOF
prte_if_include=10.0.0.0/16
btl_tcp_if_include=10.0.0.0/16

rmaps_base_allow_overload=1
rmaps_base_no_oversubscribe=0
mapby=slot

prte_default_hostfile=/shared/hostfile
EOF

cwlmpi@worker:~$ cat > /shared/hostfile <<EOF
master slots=4
worker slots=4
EOF
```

Now `mpirun` should work:

```bash
cwlmpi@master:/shared$ mpirun -np 8 --hostfile /shared/hostfile hostname
master
master
master
master
worker
worker
worker
worker
```
Follow the instructions in [`../BUILD.md`](../BUILD.md) to build FALL3D
on the `/shared/` NFS directory.

```bash
cwlmpi@master:/shared/fall3d/build$ /shared/fall3d/build/bin/Fall3d.GNU.r8.mpi.cpu.x --version
 
 FALL3D v9.1.0-dirty/HEAD
 
```

Now, the home PMIX configuration created above will fix the command line execution.
But, cwltool changes the home directory too! So you will have to patch
`/usr/lib/x86_64-linux-gnu/pmix2/share/pmix-mca-params.conf` with the
same content as PMIx's `/etc/` files are not being loaded on Ubuntu 26.04 + OpenMPI 5.x.
