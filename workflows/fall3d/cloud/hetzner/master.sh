#!/bin/bash
set -e

hostnamectl set-hostname master

apt update
DEBIAN_FRONTEND=noninteractive apt install -y nfs-kernel-server

mkdir -p /shared

chown -R cwlmpi:cwlmpi /shared
chmod 775 /shared

cat >/etc/exports <<EOF
/shared worker(rw,sync,no_subtree_check,no_root_squash)
EOF

exportfs -ra
systemctl restart nfs-kernel-server

echo
echo "=================================================="
echo "Master configuration complete."
echo
echo "MANUAL STEPS:"
echo
echo "1. Obtain worker private IP."
echo
echo "2. Add entries to /etc/hosts on BOTH machines:"
echo
echo "   <master-private-ip> master"
echo "   <worker-private-ip> worker"
echo
echo "3. Generate MPI SSH key:"
echo
echo "   sudo -u cwlmpi ssh-keygen -t ed25519"
echo
echo "4. Copy key to worker:"
echo
echo "   sudo -u cwlmpi ssh-copy-id cwlmpi@worker"
echo
echo "5. Verify:"
echo
echo "   sudo -u cwlmpi ssh worker hostname"
echo
echo "6. Create hostfile:"
echo
echo "   master slots=4"
echo "   worker slots=4"
echo
echo "7. Test MPI:"
echo
echo "   mpirun --hostfile hostfile -np 2 hostname"
echo
echo "=================================================="
