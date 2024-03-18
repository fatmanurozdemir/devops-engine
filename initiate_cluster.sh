#!/bin/bash

read -p "Enter the host IP address: " HOST_IP_ADDRESS

sudo kubeadm init --control-plane-endpoint="$HOST_IP_ADDRESS" --upload-certs --cri-socket=unix:///var/run/cri-dockerd.sock

mkdir -p $HOME/.kube
sudo touch /etc/kubernetes/admin.conf
sudo cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

sudo mkdir -p /root/.kube/
sudo cp ~/.kube/config /root/.kube/config
sudo chown root: /root/.kube/config
