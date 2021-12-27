FROM python:3.10.1
WORKDIR /opt/app
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /opt/app/src
ADD src/ .
ENTRYPOINT [ "/usr/bin/env", "python3", "." ]