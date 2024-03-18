# General Guidance

## CI/CD Pipeline Configuration

GitLab's CI/CD tool is used for configuring the pipeline effectively.

In this section, local k8s cluster is connected to Gitlab, application container images are built and pushed to Gitlab Container Registry. Then applications are deployed to the cluster pulling the images from the registry.

### Connect K8S Cluster to Gitlab.

1. Create a public Gitlab repo. 

2. Create an agent configuration file under the repo, following the guidelines provided [here.](https://docs.gitlab.com/ee/user/clusters/agent/install/index.html#create-an-agent-configuration-file)
3. Register the agent with Gitlab, following the guidelines provided [here.](https://docs.gitlab.com/ee/user/clusters/agent/install/index.html#register-the-agent-with-gitlab)
Prior to this step, ensure Helm is installed by referring to the guidelines provided [here](https://helm.sh/docs/intro/install/)

- Helm installation
    ```bash
    curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
    sudo apt-get install apt-transport-https --yes
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
    sudo apt-get update
    sudo apt-get install helm
    ```
### Container Registry 

- Authenticate to the Container Registry by using your GitLab username and password. If you have Two-Factor Authentication enabled, use a Personal Access Token instead of a password.
    ```bash
    docker login registry.gitlab.com
    ```
- Create and register gitlab project runner following guidelines provided in [here](https://docs.gitlab.com/ee/tutorials/create_register_first_runner/)

- Authorize the agent to access your projects following guidelines provided in [here](https://docs.gitlab.com/ee/user/clusters/agent/ci_cd_workflow.html#authorize-the-agent-to-access-your-projects)

- Create `.gitlab-ci.yml` file under project repository.
In gitlab-ci.yml file, build and deploy stages are included.

    
## MicroService Deployment

Two microservices are configured using flask and html.

- Build docker images for microservice 1

    ```bash
    cd microservices/hello-world-service
    docker build -t hello-world-service .
    ```

- Build docker images for microservice 2

    ```bash
    cd microservices/welcome-service
    docker build -t welcome-service .
    ```
## Istio

- Installation
    ```bash
    curl -L https://istio.io/downloadIstio | sh -
    cd istio-1.21.0
    mv bin/istioctl /usr/local/bin
    istioctl install --set profile=demo -y
    ```

- Deploy simple bookinfo microservice
    ```bash
    kubectl create -f devops-engine/manifest/bookinfo.yaml
    ```

- Deploy an Istio Ingress Gateway, to make the application accessible from the outside of the cluster
    ```bash
    kubectl create -f devops-engine/manifest/bookinfo-gateway.yaml
    ```
    
- Open the application to outside traffic
    ```bash
    cd devops-engine
    ./istio_ingress_ip_port.sh
    ```
    
## GitHub Project Integration

`devops-engine/microservices/login-page` application is used in this process.

1. Create github repo

2. Follow the instructions provided in [here](https://docs.gitlab.com/ee/ci/ci_cd_for_external_repos/github_integration.html#connect-with-personal-access-token) to connect github repo to gitlab.


3. Integrate a trigger pipeline into GitLab so that it executes whenever a push occurs within the GitHub project.

    - Access GitLab Settings: Go to your GitLab project.
    - Open CI/CD Settings: Click "Settings" > "CI/CD".
    - Add Trigger: Click "Add Trigger".
    - Configure Trigger: Name it.
    - Choose "Push events" as the trigger.
    - Click "Add Trigger".
    - Copy the provided URL.
    - Go to GitHub repository settings.
    - Add a webhook.
    - Paste the trigger URL.
    - Select "push" event.
    - Save your webhook.

4. Test application
    When you push a file to the Github repository, the Gitlab CI/CD pipeline will be triggered automatically.
