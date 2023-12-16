FROM continuumio/miniconda3

RUN mkdir -p C1_VJ279
RUN apt-get update && apt-get install -y build-essential

COPY . /C1_VJ279_clean
WORKDIR /C1_VJ279_clean

RUN conda env update --file environment.yml

RUN echo "conda activate C1_VJ279_clean" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

RUN pre-commit install
