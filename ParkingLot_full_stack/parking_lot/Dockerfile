# 当前 tensorflow 只有 cp3.6m 的编译版本...
# 而且 alpine 的 musl 替代 glibc 不能安装普通的 tf...
# 还是 debian 香...
# FROM python:3.7-alpine3.8
FROM python:3.7-stretch
RUN mkdir /project
WORKDIR /project
# debconf: unable to initialize frontend: Dialog
ENV DEBIAN_FRONTEND noninteractive
# 由 pipenv-to-requirements 生成
COPY ./requirements.txt /project
ADD ./docker-entrypoint-initenv.sh /project/docker-entrypoint-initenv.sh
# apt-get源 使用163的源
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && \
    echo "deb http://mirrors.163.com/debian/ stretch main non-free contrib" > \
			 /etc/apt/sources.list && \
    echo "deb http://mirrors.163.com/debian/ stretch-proposed-updates main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.163.com/debian/ stretch main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.163.com/debian/ stretch-proposed-updates main non-free contrib" >> /etc/apt/sources.list
# pipenv, uWSGI, django
RUN apt update -y && apt install -y \
  bash \
	git \
	apt-utils \
	build-essential \
	curl \
	# pcre \
# 	mailcap \
# 	# gcc \
# 	libc-dev \
# 	libuuid \
# 	# linux-headers \
# 	pcre-dev \
# 	jpeg-dev \
# 	zlib-dev \
# #         postgresql-dev \
# #         postgresql-client \
# #         nginx \
# 	sshpass \
# 	openssh-client \
	&& curl -sL https://deb.nodesource.com/setup_11.x | bash - \
	&& apt update -y \
	&& apt-get install -y nodejs \
	&& npm install --global yarn \
	&& pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple pip \
	# 需要提前在我的宿主机环境 pipenv run pipenv-to-requirements -f
	&& pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt \
	# && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pipenv \
	# && pipenv install --skip-lock \
	&& rm -rf /tmp/*
ENTRYPOINT ["/project/docker-entrypoint-initenv.sh"]
