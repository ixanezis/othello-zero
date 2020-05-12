#!/bin/sh
set -eu

docker run --network host --gpus all -u $(id -u):$(id -g) -v $(pwd):/home/$(whoami)/$(basename $(pwd)) -it tf
