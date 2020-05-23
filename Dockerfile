FROM tensorflow/tensorflow:latest-gpu as base

ARG USER=
ARG UID=
ARG GID=

RUN addgroup --gid $GID $USER
RUN adduser --disabled-password --gecos '' --uid $UID --gid $GID $USER
RUN usermod -aG sudo $USER

RUN apt update && apt install -y --no-install-recommends apt-utils
RUN apt update && apt install -y --no-install-recommends locales

RUN locale-gen en_US.UTF-8

RUN apt update && apt install -y --no-install-recommends \
      git \
      sudo \
      ack-grep \
      vim \
      curl

RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN curl https://bazel.build/bazel-release.pub.gpg | apt-key add -
RUN echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list

RUN apt update && apt install -y --no-install-recommends \
      bazel

USER ${UID}:${GID}
WORKDIR /home/$USER

RUN git clone --recursive https://github.com/ixanezis/configs.git
RUN ./configs/setup.sh
