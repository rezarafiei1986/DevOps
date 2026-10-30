## 1. install docker
### Add Docker Repository

```sh
sudo apt update
sudo apt install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc

sudo chmod a+r /etc/apt/keyrings/docker.asc


echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null


sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin


sudo systemctl enable --now docker
sudo docker run --rm hello-world
```



## 2- Install kubectl
kubectl is the command-line tool used to manage Kubernetes clusters.

```sh
K8S_VERSION="$(curl -L -s https://dl.k8s.io/release/stable.txt)"

curl -LO "https://dl.k8s.io/release/${K8S_VERSION}/bin/linux/amd64/kubectl"

sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
rm kubectl

kubectl version --client
```



## 3- Install Kind
Download and install the Kind binary:

```sh
KIND_VERSION="$(curl -s https://api.github.com/repos/kubernetes-sigs/kind/releases/latest | grep '"tag_name"' | cut -d '"' -f 4)"

### download kind from K8s
curl -Lo kind "https://kind.sigs.k8s.io/dl/${KIND_VERSION}/kind-linux-amd64"

### download kind from github
curl -fL --connect-timeout 15 -o kind \
  https://github.com/kubernetes-sigs/kind/releases/download/v0.33.0/kind-linux-amd64


chmod +x kind
sudo install kind /usr/local/bin/kind
rm kind

kind version
docker version
```


## 4- Create a Kubernetes cluster
Create a configuration file:

vi kind-config.yaml
```sh
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: external
networking:
  apiServerAddress: "192.168.x.x"    ## create target Kind cluster with its API endpoint bound to the target host's network IP.
  apiServerPort: 6443
nodes:
  - role: control-plane
  - role: worker
```

Save the file, then create the cluster:
```sh
kind create cluster --name lab --config kind-config.yaml
```

Kind downloads the Kubernetes node image and starts the cluster using Docker containers. The process can take several minutes.
- Verify your Kubernetes cluster
- Check the cluster context:

```sh
kubectl config get-contexts

kubectl config current-context

kubectl get nodes -o wide

kubectl get pods -A

kubectl cluster-info --context kind-lab
```
