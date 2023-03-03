# CMake generated Testfile for 
# Source directory: /home/mantaray/AUV/simulation/image_capture/opencv-4.x/modules/flann
# Build directory: /home/mantaray/AUV/simulation/image_capture/build/modules/flann
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_flann "/home/mantaray/AUV/simulation/image_capture/build/bin/opencv_test_flann" "--gtest_output=xml:opencv_test_flann.xml")
set_tests_properties(opencv_test_flann PROPERTIES  LABELS "Main;opencv_flann;Accuracy" WORKING_DIRECTORY "/home/mantaray/AUV/simulation/image_capture/build/test-reports/accuracy")
