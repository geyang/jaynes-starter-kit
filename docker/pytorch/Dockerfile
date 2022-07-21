FROM nvidia/cudagl:11.2.0-devel-ubuntu18.04

# Install python3.8
RUN apt update && apt -y install wget software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update && apt install -y python3.8 python3.8-dev python3.8-distutils
RUN ln -s `which python3.8` /usr/bin/python
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

RUN apt -y install \
    cmake \
    curl \
    git \
    tree \
    wget \
    zsh  \
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

RUN apt -y install libcgal-qt5-dev

ENV PIP_NO_CACHE_DIR=1
RUN pip install pytest pytest-forked lz4 pyyaml
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu112
RUN pip install datasets einops sklearn torchinfo tqdm

RUN apt install -y libcurl4-openssl-dev libssl-dev
RUN pip install jaynes ml-logger waterbear params-proto functional-notations
