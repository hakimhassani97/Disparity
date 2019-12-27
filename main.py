import cv2
import numpy as np
import math
import time
import random

#functions
def distance(x1,y1,x2,y2):
    # returns the z associated to point w, x1,y1 and x2,y2 are projection of w on cameras 1 and 2
    return x1-x2
    # focal=1
    # baseline=10
    # if (x1-x2)==0:
    #     s=1
    # else:
    #     s=abs(x1-x2)
    # return focal*baseline/s

def mapper2(v,mn,mx):
    # maps values [mn mx] => [0 255]
    return 255*(v-mn)/(mx-mn)

def mapper(v,t):
    # maps values [1 100] => [0 255]
    return 255*(v-min(min(t)))/(sum(max(t))/len(max(t))-min(min(t)))
    # return 255*(v-min(min(t)))/(max(max(t))-min(min(t)))
    # return 255*(v-min(t))/(max(t)-min(t))

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
                err+=(
                        abs(int(img1[y1-i//2,x1-j//2][0])-int(img2[y2-i//2,x2-j//2][0]))+
                        abs(int(img1[y1-i//2,x1-j//2][1])-int(img2[y2-i//2,x2-j//2][1]))+
                        abs(int(img1[y1-i//2,x1-j//2][2])-int(img2[y2-i//2,x2-j//2][2]))
                    )
                # err+=math.pow(
                #     math.sqrt(
                #         (int(img1[y1-i//2,x1-j//2][0])-int(img2[y2-i//2,x2-j//2][0]))**2+
                #         (int(img1[y1-i//2,x1-j//2][1])-int(img2[y2-i//2,x2-j//2][1]))**2+
                #         (int(img1[y1-i//2,x1-j//2][2])-int(img2[y2-i//2,x2-j//2][2]))**2
                #     )
                # ,2)
                pass
    return math.sqrt(err)

def bestCorrespondingBlock(x,y,img1,img2):
    # best corresponding block in img2 for pixel x,y from img1
    minim=99999
    xmin,ymin=x,y
    d=max(0,x-bestCorrespondingBlockSearchInterval)
    f=min(wr,x+bestCorrespondingBlockSearchInterval)
    for j in range(d,f,bestCorrespondingBlockSearchStep):
        d=distanceColor(x,y,img1,j,y,img2)
        # print(str(d)+' '+str(x)+' '+str(j))
        if d<minim:# and abs(x-j)<20:
            minim=d
            xmin,ymin=j,y
    return xmin,ymin

#data
# l='data/ims0.png'
# r='data/ims1.png'
l='data/lamp0.png'
r='data/lamp1.png'

#init
iml = cv2.imread(l)#,cv2.IMREAD_GRAYSCALE)
imr = cv2.imread(r)#,cv2.IMREAD_GRAYSCALE)
hl,wl,a=np.shape(iml)
hr,wr,a=np.shape(imr)
wWindow,hWindow=3,3
bestCorrespondingBlockSearchInterval=30
bestCorrespondingBlockSearchStep=5
imgStep=2

print('________________________________________')
start_time = time.time()
d=distanceColor(18,0,iml,0,0,imr)
print('err='+str(d))
x,y=bestCorrespondingBlock(142,83,iml,imr)
print('bestCorrespondingBlock : x= '+str(x)+', y= '+str(y))
#
yy=60
t=[]
ti=[]
for i in range(0,hl,imgStep):
    ti=[]
    for j in range(0,wl,imgStep):
        x,y=bestCorrespondingBlock(j,i,iml,imr)
        # print('bestCorrespondingBlock ['+str(j)+','+str(i)+'] => ['+str(x)+','+str(y)+']')
        z=distance(j,i,x,y)
        if z>=0:
            ti.append(z)
        else:
            ti.append(0)
        # print('z= '+str(z))
    t.append(ti.copy())
t2=t.copy()
mn=min(min(t))
mx=max(max(t))
# mx=sum(max(t))/len(max(t))
for i in range(0,hl//imgStep,1):
    for j in range(0,wl//imgStep,1):
        # t2[i][j]=mapper(t[i][j],t)
        t2[i][j]=mapper2(t[i][j],mn,mx)

for i in range(0,hl//imgStep,1):
    for j in range(0,wl//imgStep,1):
        # print('x= '+str(i)+', z= '+str(t2[i][j]))
        for ii in range(i*imgStep,i*imgStep+imgStep):
            for jj in range(j*imgStep,j*imgStep+imgStep):
                iml[ii][jj]=[t2[i][j],t2[i][j],t2[i][j]]

cv2.imwrite('left.png',iml)
#print(t2)
#
print("--- %s seconds ---" % (time.time() - start_time))
print('________________________________________')

cv2.namedWindow('image : '+l)
cv2.imshow('image : '+l,iml)
cv2.waitKey()
cv2.destroyAllWindows()
