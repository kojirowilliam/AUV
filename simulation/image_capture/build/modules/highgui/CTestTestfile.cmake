# CMake generated Testfile for 
# Source directory: /home/mantaray/AUV/simulation/image_capture/opencv-4.x/modules/highgui
# Build directory: /home/mantaray/AUV/simulation/image_capture/build/modules/highgui
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_highgui "/home/mantaray/AUV/simulation/image_capture/build/bin/opencv_test_highgui" "--gtest_output=xml:opencv_test_highgui.xml")
set_tests_properties(opencv_test_highgui PROPERTIES  LABELS "Main;opencv_highgui;Accuracy" WORKING_DIRECTORY "/home/mantaray/AUV/simulation/image_capture/build/test-reports/accuracy")
