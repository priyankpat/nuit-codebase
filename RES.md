https://www.learnopencv.com/install-opencv-4-on-raspberry-pi/

pip install imutils
pip install numpy
pip install PyQt4 or 5?

$ LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0 python3 Object_detection_picamera.py  --usbcam

```
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D WITH_TBB=ON \
    -D WITH_V4L=ON \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D CMAKE_SHARED_LINKER_FLAGS=-latomic \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_PYTHON3_INSTALL_PATH=/home/pi/installation/opencv-4.1.2-py3/lib/python3.5/site-packages \
    -D INSTALL_PYTHON_EXAMPLES=ON ..
```
