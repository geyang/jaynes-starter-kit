FROM python:3.8

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN bash ./aws/install

ENV PIP_NO_CACHE_DIR=1
RUN pip3 install -U pip
RUN pip3 install ipython
RUN pip3 install ml-logger jaynes cloudpickle==1.3.0