#!/bin/bash -x

REMOVE_OLD=${1:-true}
INSTALL_LATEST=${1:-true}

function yes_no_continue() {
    read -p "Are you sure? " -n 1 -r
    echo    # (optional) move to a new line
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        exit 1
    fi
}

# Ref: https://docs.docker.com/engine/install/ubuntu/

## docker

function remove_old_version_docker_tools() {
    for old in `dpkg -l | grep -i docker | awk '{print $2}'`; do
        sudo apt-get remove -y $old
    done

    sudo apt-get remove -y docker docker-engine containerd runc
}
if [ "${REMOVE_OLD}" = "true" ]; then
    remove_old_version_docker_tools
else
    echo ">>> old docker will not be removed!!!"
    docker -v
fi

function install_new_version_docker_tool() {
    sudo apt-get update -y

    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common
    
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo apt-key fingerprint 0EBFCD88
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

    sudo apt-get update -y

    sudo apt-cache policy docker-ce
    yes_no_continue
    sudo apt-get install -y \
        docker-ce \
        docker-ce-cli \
        containerd.io

    sudo systemctl start docker
    sudo systemctl enable docker

    id -nG
    sudo usermod -a -G docker ${USER}

    docker -v
    docker image ls
}
if [ "`which docker`" = "" ]; then
    install_new_version_docker_tool
else
    echo ">>> docker already installed!!!"
    docker -v
fi

## docker-compose

function install_docker_compose() {
    sudo apt remove -y docker-compose

    DOCKER_COMPOSE_RELEASE=`curl -s https://github.com/docker/compose/releases/latest | cut -d'"' -f2 | cut -d'/' -f8-`
    sudo curl -L https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_RELEASE}/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    docker-compose -v

}
if [ "${INSTALL_LATEST}" = "true" ]; then
    install_docker_compose
else
    echo ">>> docker-compose already installed!!!"
    docker-compose -v
fi

Ref: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker

# nvidia-docker

function install_nvidia_docker() {
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

    sudo apt-get update -y

    sudo apt-get install -y nvidia-docker2
    sudo systemctl restart docker
    sudo docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
}
if [ "${INSTALL_LATEST}" = "true" ]; then
    install_nvidia_docker
else
    echo ">>> docker-compose already installed!!!"
    docker-compose -v
fi

sudo apt autoremove -y
