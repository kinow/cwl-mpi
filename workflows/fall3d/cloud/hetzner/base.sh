#!/bin/bash
set -e

# This script sets up nodes for an OpenMPI installation to
# test the FALL3D Workflow. It has been successfully
# tested on two 4vCPU Intel/AMD x86 instances on Hetzner.
#
# This script contains the base software.
#
# The master node will have NFS as well. The job must
# be launched from the master.

USERNAME=cwlmpi
MAMBA_BIN="/usr/local/bin/micromamba"

echo "[0/8] System packages + MPI + NFS + containers"
apt update
DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
  openmpi-bin \
  libopenmpi-dev \
  openmpi-common \
  nfs-common \
  docker.io \
  squashfuse fuse2fs gocryptfs fuse3 apptainer \
  curl \
  bzip2 \
  openssh-server

echo "[1/8] Create non-root user"

if ! id "$USERNAME" &>/dev/null; then
    adduser --disabled-password --gecos "" $USERNAME
fi

usermod -aG sudo $USERNAME || true
usermod -aG docker $USERNAME || true

echo "[2/8] Enable SSH + Docker"
systemctl enable ssh
systemctl start ssh

systemctl enable docker
systemctl start docker

echo "[3/8] Install micromamba"

if [ -L "$MAMBA_BIN" ] || [ -f "$MAMBA_BIN" ]; then
    rm -f "$MAMBA_BIN"
fi

if [ ! -f "$MAMBA_BIN" ]; then
    echo "Downloading micromamba..."
    curl -L --fail --retry 2 -o "$MAMBA_BIN" \
      https://github.com/mamba-org/micromamba-releases/releases/download/2.5.0-2/micromamba-linux-64

    chmod +x "$MAMBA_BIN"
fi

if ! command -v micromamba &>/dev/null; then
    echo "ERROR: micromamba still not available in PATH!!!"
    ls -l /usr/local/bin/micromamba || true
    exit 1
fi

echo "micromamba OK: $(micromamba --version || true)"

mkdir -p /opt/micromamba
micromamba shell init -s bash -p /opt/micromamba || true

echo "[4/8] Setup SSH key access for user"

USER_HOME="/home/$USERNAME"
SSH_DIR="$USER_HOME/.ssh"
AUTH_KEYS="$SSH_DIR/authorized_keys"

mkdir -p "$SSH_DIR"
chmod 700 "$SSH_DIR"

touch "$AUTH_KEYS"
chmod 600 "$AUTH_KEYS"
chown -R $USERNAME:$USERNAME "$SSH_DIR"

echo "[IMPORTANT] Ensure your SSH public key is present in:"
echo "$AUTH_KEYS"

echo "[6/8] Fixing OpenMPI pmix2/prrte3 help files"

# mpirun is failing due to this OpenMPI bug:
# https://github.com/open-mpi/ompi/issues/13886
PRRTE_DIR="/usr/lib/x86_64-linux-gnu/prrte3/share/prte"
SRC_DIR="/usr/share/doc/libprrte-dev"

# These are the steps reported in the issue above that fix the mpirun error message.
mkdir -p "$PRRTE_DIR"
if [ ! -f "$PRRTE_DIR/help-schizo-ompi.txt" ]; then
    echo "Copying help-schizo-ompi.txt"
    cp "$SRC_DIR/help-schizo-ompi.txt" "$PRRTE_DIR/"
fi
if [ ! -f "$PRRTE_DIR/help-prun.txt" ] && [ -f "$SRC_DIR/help-prun.txt.gz" ]; then
    echo "Copying and decompressing help-prun.txt.gz"

    cp "$SRC_DIR/help-prun.txt.gz" "$PRRTE_DIR/"

    if [ ! -f "$PRRTE_DIR/help-prun.txt" ]; then
        gunzip -f "$PRRTE_DIR/help-prun.txt.gz"
    fi
fi

echo "[7/8] Fixing Singularity for non-privileged users"
echo "kernel.unprivileged_userns_clone=1" | sudo tee -a /etc/sysctl.d/99-apptainer.conf
echo "kernel.apparmor_restrict_unprivileged_userns=0" | sudo tee -a /etc/sysctl.d/99-apptainer.conf
sudo sysctl --system

echo "[7/8] Verify installations"

mpirun --version || true
docker --version || true
apptainer --version || true
micromamba --version || true

echo
echo "=================================================="
echo "Base installation complete."
echo
echo "Next:"
echo "  Run master.sh on the master node."
echo "  Run worker.sh on the worker node."
echo
echo "IMPORTANT:"
echo
echo "After the installation of master and worker, add"
echo "this to fix a problem with OpenMPI MPI startup:"
echo
echo "export OMPI_MCA_btl_tcp_if_include=10.0.0.0/12"
echo "export OMPI_MCA_oob_tcp_if_include=10.0.0.0/12"
echo "export PRTE_MCA_oob_tcp_if_include=10.0.0.0/12"
echo
echo "=================================================="
