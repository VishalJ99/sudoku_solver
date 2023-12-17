FROM continuumio/miniconda3

RUN mkdir -p /C1_VJ279
RUN apt-get update && apt-get install -y build-essential

COPY . /C1_VJ279
WORKDIR /C1_VJ279

# Update conda environment
RUN conda env update --file environment.yml

# Initialize conda for shell interaction
RUN conda init bash

# Activate the environment by default
ENV PATH /opt/conda/envs/C1_VJ279/bin:$PATH

# Install pre-commit
RUN pre-commit install
