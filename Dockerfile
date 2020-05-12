FROM tensorflow/tensorflow:latest-gpu as base

ARG USER=
ARG UID=
ARG GID=

RUN addgroup --gid $GID $USER
RUN adduser --disabled-password --gecos '' --uid $UID --gid $GID $USER
RUN usermod -aG sudo $USER
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN apt update && apt install -y --no-install-recommends apt-utils
RUN apt update && apt install -y --no-install-recommends locales

RUN locale-gen en_US.UTF-8

RUN rm /etc/sudoers

RUN apt update && apt install -y --no-install-recommends \
      git \
      sudo \
      ack-grep \
      vim

USER ${UID}:${GID}
WORKDIR /home/$USER

RUN git clone --recursive https://github.com/ixanezis/configs.git
RUN ./configs/setup.sh
