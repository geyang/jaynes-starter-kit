FROM nvidia/cudagl:11.3.0-devel-ubuntu18.04

FROM python:3.8
ENV PIP_NO_CACHE_DIR=1
RUN apt update
RUN yes | apt install \
    tree \
    zsh  \
    git \
    cmake \
    build-essential \
    libboost-program-options-dev \
    libboost-filesystem-dev \
    libboost-graph-dev \
    libboost-system-dev \
    libboost-test-dev \
    libeigen3-dev \
    libsuitesparse-dev \
    libfreeimage-dev \
    libmetis-dev \
    libgoogle-glog-dev \
    libgflags-dev \
    libglew-dev \
    qtbase5-dev \
    libqt5opengl5-dev \
    libcgal-dev

RUN yes | apt install libcgal-qt5-dev
RUN pip install --upgrade pip
RUN pip install pytest pytest-forked lz4 pyyaml
RUN pip install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install datasets einops sklearn torchinfo tqdm
RUN pip install jaynes ml-logger waterbear params-proto functional-notations