FROM amazonlinux:2.0.20190115
MAINTAINER Quilt Data, Inc. contact@quiltdata.io

RUN yum install -y gettext
RUN amazon-linux-extras install nginx1.12

COPY nginx-quilt.conf /etc/nginx/nginx.conf

CMD nginx -g "daemon off;"
