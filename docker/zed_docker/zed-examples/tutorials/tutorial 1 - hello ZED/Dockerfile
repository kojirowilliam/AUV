# FROM stereolabs/zed:3.7-gl-devel-cuda11.4-ubuntu20.04
# FROM stereolabs/zed:3.0-devel-jetson-jp4.2
FROM stereolabs/zed:3.8-tools-devel-jetson-jp5.0.2

# Set the working directory
WORKDIR /app

# Copy files from your host to your current working directory
COPY cpp hello_zed_src

RUN apt-get update && apt-get install -y libssl-dev && apt-get update && apt-get -y install cmake

# RUN wget https://github.com/Kitware/CMake/releases/download/v3.25.1/cmake-3.25.1.tar.gz && \
#     tar -xf cmake-3.25.1.tar.gz && cd cmake-3.25.1 && ./configure && make install

# Build the application with cmake
# mkdir /app/hello_zed_src/build && cd /app/hello_zed_src/build && cmake -DCMAKE_LIBRARY_PATH=/usr/local/cuda/lib64/stubs -DCMAKE_CXX_FLAGS="-Wl,--allow-shlib-undefined" .. && make
# RUN mkdir /app/hello_zed_src/build && cd /app/hello_zed_src/build && \
#    cmake -DCMAKE_LIBRARY_PATH=/usr/local/cuda/lib64/stubs \
#      -DCMAKE_CXX_FLAGS="-Wl,--allow-shlib-undefined" .. && \
#    make

# # Run the application
# CMD ["/app/hello_zed_src/build/ZED_Tutorial_1"]
