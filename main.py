import cv2
import numpy as np
import math
import sys
#test images
# s='test.png'
s='lenna.jpg'
# s='test2.png'
# s='test4.jpg'
# s='ttt.jpg'

regions=[]
region=[]
visited=[]
seuil=8
# sys.setrecursionlimit(1000000000)
def diff(img,x1,y1,x2,y2):
    db=int(img[y2][x2][0])-int(img[y1][x1][0])
    dg=int(img[y2][x2][1])-int(img[y1][x1][1])
    dr=int(img[y2][x2][2])-int(img[y1][x1][2])
    d=math.sqrt(math.pow(db,2)+math.pow(dg,2)+math.pow(dr,2))
    return d

def drawRegion(img,region):
    for i in region:
        x,y=i
        img[y][x][2]=0
        img[y][x][1]=0
        img[y][x][0]=200

def grow(img,x,y):
    visited=[]
    toVisit=[[x,y]]
    region.append([x,y])
    while len(toVisit)>0:
        i=toVisit[0]
        if not i in visited:
            if(i[0]<w-1):
                if diff(img,i[0],i[1],i[0]+1,i[1])<seuil:
                    region.append([i[0]+1,i[1]])
                    if not [i[0]+1,i[1]] in toVisit or not [i[0]+1,i[1]] in visited:
                        toVisit.append([i[0]+1,i[1]])
            if(i[1]<h-1):
                if diff(img,i[0],i[1],i[0],i[1]+1)<seuil:
                    region.append([i[0],i[1]+1])
                    if not [i[0],i[1]+1] in toVisit or not [i[0],i[1]+1] in visited:
                        toVisit.append([i[0],i[1]+1])
            if(i[0]>0):
                if diff(img,i[0],i[1],i[0]-1,i[1])<seuil:
                    region.append([i[0]-1,i[1]])
                    if not [i[0]-1,i[1]] in toVisit or not [i[0]-1,i[1]] in visited:
                        toVisit.append([i[0]-1,i[1]])
            if(i[1]>0):
                if diff(img,i[0],i[1],i[0],i[1]-1)<seuil:
                    region.append([i[0],i[1]-1])
                    if not [i[0],i[1]-1] in toVisit or not [i[0],i[1]-1] in visited:
                        toVisit.append([i[0],i[1]-1])
            visited.append(i)
        toVisit.remove(i)

def growRec(img,x,y):
    if not [x,y] in visited:
        visited.append([x,y])
        # if x>0 and x<w-1 and y>0 and y<h-1:
        if(x<w-1):
            if diff(img,seedX,seedY,x+1,y)<seuil:
                region.append([x+1,y])
                grow(img,x+1,y)
        if(y<h-1):
            if diff(img,seedX,seedY,x,y+1)<seuil:
                region.append([x,y+1])
                grow(img,x,y+1)
        if(x>0):
            if diff(img,seedX,seedY,x-1,y)<seuil:
                region.append([x-1,y])
                grow(img,x-1,y)
        if(y>0):
            if diff(img,seedX,seedY,x,y-1)<seuil:
                region.append([x,y-1])
                grow(img,x,y-1)
    return

def on_mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        img=np.copy(original)
        grow(img,x,y)
        drawRegion(img,region)
        cv2.imshow('image : '+s,img)
        
#init
original = cv2.imread(s)
img = cv2.imread(s)
h,w,d=np.shape(img)
#begin
seedX,seedY=0,0
# grow(img,0,0)
# drawRegion(img,region)
# print(diff(img,0,0,1,1))
cv2.namedWindow('image : '+s)
cv2.setMouseCallback('image : '+s, on_mouse, 0, )
cv2.imshow('image : '+s,img)
cv2.waitKey()
cv2.destroyAllWindows()