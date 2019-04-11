FROM python:3.7.0-alpine3.8
RUN mkdir /project
WORKDIR /project
# 备份
RUN cp /etc/apk/repositories /etc/apk/repositories.bak
# 修改为国内镜像源
RUN echo "http://mirrors.aliyun.com/alpine/v3.8/main/" > /etc/apk/repositories
# pipenv, uWSGI, django
RUN apk update && apk add --no-cache \
        bash \
        pcre \
        mailcap \
        # gcc \
        libc-dev \
        libuuid \
        # linux-headers \
        pcre-dev \
        jpeg-dev \
        zlib-dev \
        musl-dev \
#         postgresql-dev \
#         postgresql-client \
#         nginx \
        sshpass \
	openssh-client \
    && pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple pip \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pipenv \
    && pipenv install --skip-lock \
    && apk del \
        # gcc \
        libc-dev \
        # linux-headers \
    && rm -rf /tmp/*
