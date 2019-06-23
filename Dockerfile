# Pull base image.
FROM ubuntu:18.04

# sudo access
RUN apt-get update && \
      apt-get -y install sudo
#RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

RUN sudo apt-get update
RUN sudo apt-get -y install python3-pip
RUN pip3 install tensorflow
RUN pip3 install keras
RUN sudo apt-get -y install git-core
RUN pip3 install numpy scipy pandas
RUN git clone https://github.com/ai-personas/ai-personas.git
RUN cd ai-personas

EXPOSE 80



