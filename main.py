import cv2
import numpy as np
import math
import time

#functions
def distanceGrayScale(x1,y1,img1,x2,y2,img2):
    # distance between x1,y in img1 and x2,y2 in img2
    err=0.0
    for i in range(0,hWindow):
        for j in range(0,wWindow):
            if (y1-i//2>=0 and x1-j//2>=0 and y2-i//2>=0 and x2-j//2>=0) and (y1-i//2<hl and x1-j//2<wl and y2-i//2<hr and x2-j//2<wr):
                err+=math.pow(int(img1[y1-i//2,x1-j//2])-int(img2[y2-i//2,x2-j//2]),2)
            pass
    return math.sqrt(err)

def distanceColor(x1,y1,img1,x2,y2,img2):
    # distance between x1,y in img1 and x2,y2 in img2
    err=0.0
    for i in range(0,hWindow):
        for j in range(0,wWindow):
            if (y1-i//2>=0 and x1-j//2>=0 and y2-i//2>=0 and x2-j//2>=0) and (y1-i//2<hl and x1-j//2<wl and y2-i//2<hr and x2-j//2<wr):
                err+=math.pow(
                    math.sqrt(
                        (int(img1[y1-i//2,x1-j//2][0])-int(img2[y2-i//2,x2-j//2][0]))**2+
                        (int(img1[y1-i//2,x1-j//2][1])-int(img2[y2-i//2,x2-j//2][1]))**2+
                        (int(img1[y1-i//2,x1-j//2][2])-int(img2[y2-i//2,x2-j//2][2]))**2
                    )
                ,2)
            pass
    return math.sqrt(err)

def bestCorrespondingBlock(x,y,img1,img2):
    # best corresponding block in img2 for pixel x,y from img1
    minim=99999
    xmin,ymin=0,0
    for j in range(0,wr):
        d=distanceColor(x,y,img1,j,y,img2)
        # print(str(d)+' '+str(x)+' '+str(j))
        if d<minim:
            minim=d
            xmin,ymin=j,y
    return xmin,ymin

#data
l='data/im0.png'
r='data/im1.png'
# l='0.png'
# r='1.png'

#init
iml = cv2.imread(l)#,cv2.IMREAD_GRAYSCALE)
imr = cv2.imread(r)#,cv2.IMREAD_GRAYSCALE)
hl,wl,a=np.shape(iml)
hr,wr,a=np.shape(imr)
wWindow,hWindow=16,16

print('________________________________________')
start_time = time.time()
d=distanceColor(18,0,iml,0,0,imr)
print('err='+str(d))
x,y=bestCorrespondingBlock(0,0,imr,iml)
print('bestCorrespondingBlock : x= '+str(x)+', y= '+str(y))
print("--- %s seconds ---" % (time.time() - start_time))
print('________________________________________')

cv2.namedWindow('image : '+l)
cv2.imshow('image : '+l,iml)
cv2.waitKey()
cv2.destroyAllWindows()
