FROM nvidia/cudagl:11.6.0-devel-ubuntu20.04

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
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
RUN pip install datasets einops sklearn torchinfo tqdm
RUN pip install jaynes ml-logger waterbear params-proto functional-notations