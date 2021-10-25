FROM centos:8
RUN  yum update -y && \
  yum install -y \
    git-2.27.0-1.el8.x86_64 python36-3.6.8-2.module_el8.4.0+790+083e3d81.x86_64 python3-pip-9.0.3-19.el8.noarch python3-flask.noarch python3-requests yum-utils

RUN yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo

RUN yum install -y docker-ce docker-ce-cli containerd.io

RUN curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose
