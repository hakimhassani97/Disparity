import cv2
import numpy as np
import math

def distance(x1,y1,img1,x2,y2,img2):
    err=0.0
    for i in range(0,hWin):
        for j in range(0,wWin):
            err+=math.pow(int(img1[y1-i//2,x1-j//2])-int(img2[y2-i//2,x2-j//2]),2)
            pass
    return math.sqrt(err)

l='im0.png'
r='im1.png'
# l='0.png'
# r='1.png'

#init
iml = cv2.imread(l,cv2.IMREAD_GRAYSCALE)
imr = cv2.imread(r,cv2.IMREAD_GRAYSCALE)
hl,wl=np.shape(iml)
hr,wr=np.shape(imr)
wWin,hWin=16,16

d=distance(18,0,iml,0,0,imr)
print('err='+str(d))

cv2.namedWindow('image : '+l)
cv2.imshow('image : '+l,iml)
cv2.waitKey()
cv2.destroyAllWindows()