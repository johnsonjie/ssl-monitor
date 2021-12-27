FROM python:3.7

RUN echo "Asia/Shanghai" > /etc/timezone
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
WORKDIR /ssl-cert-exporter
COPY . .
VOLUME /ssl-cert-exporter/config
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
#EXPOSE 8000
CMD python domain-ssl-gauge.py
