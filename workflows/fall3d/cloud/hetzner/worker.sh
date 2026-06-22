#!/bin/bash
set -e

hostnamectl set-hostname worker

mkdir -p /shared

echo
echo "=================================================="
echo "Worker configuration complete."
echo
echo "MANUAL STEP:"
echo
echo "After /etc/hosts has been configured,"
echo "mount the master's NFS export:"
echo
echo "  mount master:/shared /shared"
echo
echo "To make it permanent add:"
echo
echo "  master:/shared /shared nfs defaults,_netdev 0 0"
echo
echo "to /etc/fstab"
echo
echo "=================================================="
