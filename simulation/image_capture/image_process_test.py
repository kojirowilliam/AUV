import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")



while True:
	ret, frame = cap.read()
	frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
	orb = cv2.ORB_create()
	orb.setEdgeThreshold(1)
	kp = orb.detect(frame,None)
	img2 = cv2.drawKeypoints(frame, kp, None, color=(0,255,0), flags=0)
        cv2.imshow('Input', img2)
        c = cv2.waitKey(10)
	if c == 27:
		break

cap.release()
cv2.destroyAllWindows()


cv_image = cv2.imread('moms5_4x3.png', cv2.IMREAD_GRAYSCALE)
#cv2.imshow('win', cv_image)
width = cv_image.shape[0]
length = cv_image.shape[1]
resize = cv2.resize(cv_image, (width/3, length/3))
#cv2.imshow('resize', resize)
img_blur = cv2.GaussianBlur(resize, (3,3), 0)
edges = cv2.Canny(image = cv_image, threshold1 = 100, threshold2 = 200)
#cv2.imshow('edge', edges)



