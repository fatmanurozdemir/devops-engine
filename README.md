# devops-engine

This project involves setting up a CI/CD pipeline using Kubernetes and Istio for managing microservices deployments. It includes configuring Kubernetes clusters, integrating CI/CD tools with version control systems, containerizing microservices with Docker, configuring Istio for service mesh functionalities, deploying open-source solutions, integrating GitHub projects, and implementing monitoring/logging solutions. Detailed documentation is provided for easy setup and smooth operation of the applications.

## Kubernetes Cluster Setup

### Install docker

```bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl enable docker
sudo systemctl status docker
sudo usermod -aG docker $USER
sudo reboot
```

### Install kubeadm

The installation of `kubeadm` follows the guidelines provided in the official Kubernetes documentation [here](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/).

The entire project is conducted on an Ubuntu 22.04 computer.

1. Update the apt package index and install packages needed to use the Kubernetes apt repository:

    ```bash
    sudo apt-get update
    # apt-transport-https may be a dummy package; if so, you can skip that package
    sudo apt-get install -y apt-transport-https ca-certificates curl gpg
    ```
    
2. Download the public signing key for the Kubernetes package repositories. The same signing key is used for all repositories so you can disregard the version in the URL:
    ```bash
    # If the directory `/etc/apt/keyrings` does not exist, it should be created before the curl command, read the note below.
    # sudo mkdir -p -m 755 /etc/apt/keyrings
    curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
    ```
    
3. Add the appropriate Kubernetes apt repository. 
    ```bash
    echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/adeb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
    ```
    
4. Update the apt package index, install kubelet, kubeadm and kubectl, and pin their version:

    ```bash
    sudo apt-get update
    sudo apt-get install -y kubelet kubeadm kubectl
    sudo apt-mark hold kubelet kubeadm kubectl
    ```
5. Disable swap

    ```bash
    sudo swapoff -a
    sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
    sudo service kubelet restart
    ```

6. K8s Autocompletion

- Add following lines to the `~/.bashrc`:
    ```bash
    source <(kubectl completion bash)
    alias k=kubectl
    complete -F __start_kubectl k
    ```
- Then execute `source ~/.bashrc`

### Install Container Runtime(cri-dockerd)

```bash
wget https://github.com/Mirantis/cri-dockerd/releases/download/v0.3.9/cri-dockerd_0.3.9.3-0.ubuntu-jammy_amd64.deb
dpkg -i cri-dockerd_0.3.9.3-0.ubuntu-jammy_amd64.deb
```

### Cluster Initialization

- Initialize cluster with kubeadm and configure `kubectl` to communicate with the Kubernetes cluster initialized using `kubeadm`. They ensure that both the current user and the root user can access the Kubernetes configuration file.
    ```bash
    ./initiate_cluster.sh
    ```

### Cluster Networking

- Deploy calico CNI plugin for cluster networking

    ```bash
    kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/master/manifests/tigera-operator.yaml
    kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/master/manifests/calico.yaml
    kubectl taint nodes --all node-role.kubernetes.io/control-plane-
    ```
