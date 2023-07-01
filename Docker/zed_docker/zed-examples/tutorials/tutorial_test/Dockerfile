FROM stereolabs/zed:3.8-tools-devel-jetson-jp5.0.2

WORKDIR /app

COPY cpp hello_zed_src

RUN mkdir /app/hello_zed_src/build && cd /app/hello_zed_src/build
RUN apt-get update && apt-get install -y cmake
# && cmake -DCMAKE_LIBRARY_PATH=/usr/local/cuda/lib64/stubs -DCMAKE_CXX_FLAGS="-Wl,--allow-shlib-undefined" .. \
# && make
CMD ["../bin/sh"]
# CMD ["/app/hello_zed_src/build/ZED_Tutorial_1"]
