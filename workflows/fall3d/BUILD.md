# Compilation of FALL3D

## FT3

```bash
$ # FALL3D was not compiled on FT3 due to the VPN being offline at the time
$ # of the compilation -- a vulnerability in the SNX VPN software on Linux.
```

## LUMI

```bash
cd /pfs/lustrep4/projappl/[REDACTED]/[REDACTED]/
git clone -o upstream https://gitlab.com/fall3d-suite/fall3d.git
cd fall3d
module load cray-hdf5 cray-netcdf
module list

Currently Loaded Modules:
  1) craype-x86-rome          5) xpmem/2.11.5-1.3_g73ade43320bc   9) cray-mpich/8.1.32        13) lumi-tools/26.05     (S)
  2) libfabric/1.22.0         6) cce/19.0.0                      10) cray-libsci/25.03.0      14) init-lumi/0.2        (S)
  3) craype-network-ofi       7) craype/2.7.34                   11) PrgEnv-cray/8.6.0        15) cray-hdf5/1.12.2.11
  4) perftools-base/25.03.0   8) cray-dsmml/0.3.1                12) ModuleLabel/label   (S)  16) cray-netcdf/4.9.0.11

  Where:
   S:  Module is Sticky, requires --force to unload or purge
rm -rf build
mkdir build
cd build
cmake .. \
  -DDETAIL_BIN=YES \
  -DWITH-MPI=YES \
  -DWITH-ACC=NO \
  -DWITH-R4=NO
make -j8
file /pfs/lustrep4/projappl/[REDACTED]/[REDACTED]/fall3d/build/bin/Fall3d.Cray.r8.mpi.cpu.x
/pfs/lustrep4/projappl/[REDACTED]/[REDACTED]/fall3d/build/bin/Fall3d.Cray.r8.mpi.cpu.x: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 4.3.0, with debug_info, not stripped
micromamba run -n python-3.13 cwltool --debug fall3d-what-if-volcanos.0.2.1.cwl#demo-etna arguments_etna.yml
micromamba run -n python-3.13 cwltool --singularity --debug fall3d-what-if-volcanos.0.2.1.cwl#demo-etna arguments_etna.yml
```

## MN5

```bash
cd /gpfs/projects/[REDACTED]/[REDACTED]/
git clone -o upstream https://gitlab.com/fall3d-suite/fall3d.git
cd fall3d
module load EB/apps
# Intel compiler + MPI
module load intel/2023.2.0
module load impi/2021.10.0
# Intel-built NetCDF (Fortran + C)
module load netCDF/4.9.2-iimpi-2023a
module load netCDF-Fortran/4.6.1-iimpi-2023a
# CMake built with GCCcore 13 (runtime matches)
module load CMake/3.27.6-GCCcore-13.2.0
module list

Currently Loaded Modules:
  1) intel/2023.2.0              13) cURL/8.3.0-GCCcore-13.2.0         25) libfabric/1.19.0-GCCcore-13.2.0
  2) impi/2021.10.0              14) XZ/5.4.4-GCCcore-13.2.0           26) PMIx/4.2.6-GCCcore-13.2.0
  3) mkl/2023.2.0                15) libarchive/3.7.2-GCCcore-13.2.0   27) UCC/1.2.0-GCCcore-13.2.0
  4) ucx/1.15.0                  16) CMake/3.27.6-GCCcore-13.2.0       28) OpenMPI/4.1.6-GCC-13.2.0
  5) oneapi/2023.2.0             17) binutils/2.40-GCCcore-13.2.0      29) gompi/2023b
  6) bsc/1.0                     18) GCC/13.2.0                        30) Szip/2.1.1-GCCcore-13.2.0
  7) EB/apps                     19) numactl/2.0.16-GCCcore-13.2.0     31) HDF5/1.14.3-gompi-2023b
  8) GCCcore/13.2.0              20) libxml2/2.11.5-GCCcore-13.2.0     32) gzip/1.13-GCCcore-13.2.0
  9) ncurses/6.4-GCCcore-13.2.0  21) libpciaccess/0.17-GCCcore-13.2.0  33) lz4/1.9.4-GCCcore-13.2.0
 10) zlib/1.2.13-GCCcore-13.2.0  22) hwloc/2.9.2-GCCcore-13.2.0        34) zstd/1.5.5-GCCcore-13.2.0
 11) bzip2/1.0.8-GCCcore-13.2.0  23) libevent/2.1.12-GCCcore-13.2.0    35) netCDF/4.9.2-gompi-2023b
 12) OpenSSL/1.1                 24) UCX/1.15.0-GCCcore-13.2.0         36) netCDF-Fortran/4.6.1-gompi-2023b
rm -rf build
mkdir build
cd build
cmake .. \
    -DDETAIL_BIN=YES \
    -DWITH-MPI=YES \
    -DWITH-ACC=NO \
    -DWITH-R4=NO
make -j8
file /gpfs/projects/[REDACTED]/[REDACTED]/fall3d/build/bin/Fall3d.Intel.r8.mpi.cpu.x
/gpfs/projects/[REDACTED]/[REDACTED]/fall3d/build/bin/Fall3d.Intel.r8.mpi.cpu.x: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=2583dc9de301bd38d381ac78f7c65a448c737dfc, for GNU/Linux 3.2.0, not stripped
```

## Laptop & Cloud

```bash
cd /home/kinow/Development/fortran/workspace
git clone -o upstream https://gitlab.com/fall3d-suite/fall3d.git --branch=9.1.0 --single-branch --depth=1
cd fall3d
sudo apt install -y \
    build-essential \
    gfortran \
    cmake \
    git \
    mpich \
    libnetcdf-dev \
    libnetcdff-dev \
    pkg-config
kinow@ranma:~/Development/fortran/workspace/fall3d$ cmake --version
cmake version 4.2.3

CMake suite maintained and supported by Kitware (kitware.com/cmake).
kinow@ranma:~/Development/fortran/workspace/fall3d$ mpif90 --version
GNU Fortran (Ubuntu 15.2.0-16ubuntu1) 15.2.0
Copyright (C) 2025 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

kinow@ranma:~/Development/fortran/workspace/fall3d$ nf-config --version
netCDF-Fortran 4.6.2
kinow@ranma:~/Development/fortran/workspace/fall3d$ nc-config --version
netCDF 4.9.3
 nf-config --all

This netCDF-Fortran 4.6.2 has been built with the following features: 

  --cc        -> gcc
  --cflags    -> -I/usr/include -Wdate-time -D_FORTIFY_SOURCE=3

  --fc        -> gfortran
  --fflags    -> -I/usr/include -I/usr/include
  --flibs     -> -L/usr/lib/x86_64-linux-gnu -lnetcdff -Wl,-Bsymbolic-functions -Wl,--package-metadata=%7B%22type%22:%22deb%22%2C%22os%22:%22ubuntu%22%2C%22name%22:%22netcdf-fortran%22%2C%22version%22:%224.6.2+ds-1%22%2C%22architecture%22:%22amd64%22%7D -flto=auto -ffat-lto-objects -Wl,-z,relro -Wl,-z,now -lnetcdf -lnetcdf -lm 
  --has-f90   -> 
  --has-f03   -> yes

  --has-nc2   -> yes
  --has-nc4   -> yes

  --prefix    -> /usr
  --includedir-> /usr/include
  --version   -> netCDF-Fortran 4.6.2
# Fix MPI compile flags handling in CMakeLists.txt:
# MPICH exposes MPI_Fortran_COMPILE_FLAGS as a single space-separated string.
# CMake incorrectly treats it as one argument when quoted, causing gfortran to
# receive a single "giant flag" string instead of individual flags.
# separate_arguments() splits it into a proper CMake list so each compiler flag
# is passed correctly to the Fortran compiler.
sed -i 's/list(APPEND COMPILER_FLAGS "\${MPI_Fortran_COMPILE_FLAGS}" "-DWITH_MPI")/separate_arguments(MPI_Fortran_COMPILE_FLAGS)\nlist(APPEND COMPILER_FLAGS ${MPI_Fortran_COMPILE_FLAGS} "-DWITH_MPI")/' CMakeLists.txt
rm -rf build
mkdir build
cd build
cmake .. \
    -DDETAIL_BIN=YES \
    -DWITH-MPI=YES \
    -DWITH-ACC=NO \
    -DWITH-R4=NO
make -j4
file /home/kinow/Development/fortran/workspace/fall3d/build/bin/Fall3d.GNU.r8.mpi.cpu.x
/home/kinow/Development/fortran/workspace/fall3d/build/bin/Fall3d.GNU.r8.mpi.cpu.x: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=73687acf1728ca9ec88cd0861e67c7c1029095ed, for GNU/Linux 3.2.0, not stripped
```

To verify the installation:

```bash
cd ../
mkdir work
cd work
cp ../Templates/template.inp Example.inp
wget https://gitlab.geo3bcn.csic.es/fall3d/what-if-demo/-/raw/aa34846e748422c32194e388a508d7cec8c68cc8/Example.wrf.nc
cp ../Other/Meteo/Tables/WRF.tbl .
/home/kinow/Development/fortran/workspace/fall3d/build/bin/Fall3d.GNU.r8.mpi.cpu.x All Example.inp
/
home/kinow/Development/fortran/workspace/fall3d/build/bin/Fall3d.GNU.r8.mpi.cpu.x All Example.inp
       ______      _      _      ____  _____           
      |  ____/\   | |    | |    |___ \|  __ \          
      | |__ /  \  | |    | |      __) | |  | |         
      |  __/ /\ \ | |    | |     |__ <| |  | |         
      | | / ____ \| |____| |____ ___) | |__| |         
      |_|/_/    \_\______|______|____/|_____/          
                                                       
                                                       
             Initializing FALL3D suite                 
Copyright: 2018 GNU General Public License version 3
(see licence for details)
Version               : 9.1.0-dirty/HEAD Hardware              : General Purpose (CPU) Compiler              : GCC version 15.2.0 Input File            : Example.inp Number of processors  : 00001 Number of sub-domains : 00001 x 00001 x 00001 Number of instances   : 00001

 Running SetTgsd task...  Running SetDbs task...  Running SetSrc task...  Running FALL3D solver...  The program has been run successfully

less Example.Fall3d.log
```
