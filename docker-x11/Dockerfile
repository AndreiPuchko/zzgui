FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Add user
RUN adduser --quiet --disabled-password zzgui && usermod -a -G audio zzgui

# This fix: libGL error: No matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1

# Install Python 3, PyQt5
RUN apt-get update && apt-get install -y python3-pyqt5
RUN apt-get install -y git && apt-get install -y python3-pip && pip3 install zzdb
RUN cd /home/zzgui && git clone https://github.com/AndreiPuchko/zzgui.git
WORKDIR /home/zzgui/zzgui
