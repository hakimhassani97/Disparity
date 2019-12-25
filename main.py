import cv2
import numpy as np
import math
import time

#functions
def distance(x1,y1,img1,x2,y2,img2):
    err=0.0
    for i in range(0,hWindow):
        for j in range(0,wWindow):
            if y1-i//2>=0 and x1-j//2>=0 and y2-i//2>=0 and x2-j//2>=0:
                err+=math.pow(int(img1[y1-i//2,x1-j//2])-int(img2[y2-i//2,x2-j//2]),2)
            pass
    return math.sqrt(err)

#data
l='data/im0.png'
r='data/im1.png'
# l='0.png'
# r='1.png'

#init
iml = cv2.imread(l,cv2.IMREAD_GRAYSCALE)
imr = cv2.imread(r,cv2.IMREAD_GRAYSCALE)
hl,wl=np.shape(iml)
hr,wr=np.shape(imr)
wWindow,hWindow=16,16

start_time = time.time()
d=distance(18,0,iml,0,0,imr)
print("--- %s seconds ---" % (time.time() - start_time))
print('err='+str(d))

cv2.namedWindow('image : '+l)
cv2.imshow('image : '+l,iml)
cv2.waitKey()
cv2.destroyAllWindows()