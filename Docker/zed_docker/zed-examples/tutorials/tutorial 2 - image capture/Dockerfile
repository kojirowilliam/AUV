FROM stereolabs/zed:3.8-tools-devel-jetson-jp5.0.2
WORKDIR /app
COPY cpp image_capture_src
RUN apt-get update && apt-get -y install cmake
