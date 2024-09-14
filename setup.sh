#!/bin/bash

sudo apt-get update
sudo apt install qemu-kvm libvirt-daemon-system libvirt-dev
sudo apt install netcat-traditional
sudo systemctl start libvirtd
sudo virsh net-start default