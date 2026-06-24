FROM docker.io/ubuntu:24.04

ARG libfabric_version=1.22.0
ARG mpi_version=4.3.1
ARG osu_version=7.5.1

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        automake \
        autoconf \
        libtool \
        make \
        gdb \
        strace \
        wget \
        python3 \
        git \
        gfortran \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/hpc/xpmem \
    && cd xpmem/lib \
    && gcc -I../include -shared -o libxpmem.so.1 libxpmem.c \
    && ln -s libxpmem.so.1 libxpmem.so \
    && mv libxpmem.so* /usr/lib64 \
    && cp ../include/xpmem.h /usr/include/ \
    && ldconfig \
    && cd ../../ \
    && rm -rf xpmem

RUN wget -q \
        https://github.com/ofiwg/libfabric/archive/v${libfabric_version}.tar.gz \
    && tar xf v${libfabric_version}.tar.gz \
    && cd libfabric-${libfabric_version} \
    && ./autogen.sh \
    && ./configure \
        --prefix=/usr \
    && make -j"$(nproc)" \
    && make install \
    && ldconfig \
    && cd .. \
    && rm -rf \
        v${libfabric_version}.tar.gz \
        libfabric-${libfabric_version}

RUN wget -q \
        https://www.mpich.org/static/downloads/${mpi_version}/mpich-${mpi_version}.tar.gz \
    && tar xf mpich-${mpi_version}.tar.gz \
    && cd mpich-${mpi_version} \
    && ./autogen.sh \
    && ./configure \
        --prefix=/usr \
        --enable-fast=O3,ndebug \
        --enable-fortran \
        --enable-cxx \
        --with-device=ch4:ofi \
        --with-libfabric=/usr \
        --with-xpmem=/usr \
    && make -j"$(nproc)" \
    && make install \
    && ldconfig \
    && cd .. \
    && rm -rf \
        mpich-${mpi_version}.tar.gz \
        mpich-${mpi_version}

RUN wget -q \
        http://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-v${osu_version}.tar.gz \
    && tar xf osu-micro-benchmarks-v${osu_version}.tar.gz \
    && cd osu-micro-benchmarks-v${osu_version} \
    && ./configure \
        --prefix=/usr/local \
        CC="$(which mpicc)" \
        CFLAGS=-O3 \
    && make -j"$(nproc)" \
    && make install \
    && cd .. \
    && rm -rf \
        osu-micro-benchmarks-v${osu_version} \
        osu-micro-benchmarks-v${osu_version}.tar.gz \
