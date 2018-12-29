import tkinter
from tkinter import filedialog
from tkinter.constants import *
import numpy as np
import argparse
import cv2
import imutils
import os
img = ''

def bf():
    global img
    img = filedialog.askopenfilename()
    pathlabel.config(text=os.path.basename(img))

tk = tkinter.Tk()
frame = tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)
label = tkinter.Label(frame, text='')
label.pack(fill=X, expand=1)
pathlabel = tkinter.Label(frame)
button = tkinter.Button(frame,text="browse",command=bf)
button1 = tkinter.Button(frame,text="analyse",command=tk.destroy)

pathlabel.pack(side=TOP)

button.pack(side=TOP)
button1.pack(side=BOTTOM)
tk.mainloop()


image = cv2.imread(os.path.basename(img))
img_hsv=cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_red = np.array([0,50,50])
upper_red = np.array([10,255,255])
mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

lower_red = np.array([170,50,50])
upper_red = np.array([180,255,255])
mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

mask = mask0+mask1

output_img = image.copy()
output_img[np.where(mask==0)] = 0

output_hsv = img_hsv.copy()
output_hsv[np.where(mask==0)] = 0

img = output_img.astype(np.int16)

img_b = img[:, :, 0]
img_g = img[:, :, 1]
img_r = img[:, :, 2]

res_br = img_r - img_b
res_gr = img_r - img_g
res = np.maximum(res_br, res_gr)
res[res < 0] = 0
res = res.astype(np.uint8)

blurred = cv2.GaussianBlur(res, (3, 3), 0)#for smoothing, may remove
erode = cv2.erode(blurred,None,iterations = 12)
dilate = cv2.dilate(erode,None,iterations = 5)
#

ret, thresh = cv2.threshold(dilate, 50, 1, cv2.THRESH_BINARY)

_,contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
cv2.CHAIN_APPROX_SIMPLE)

print(len(contours))

cnts = cv2.findContours(thresh.copy(),
cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
i=0
for c in cnts:
    #cv2.drawContours(output_img, [c], -1, (0, 255, 0), 2)
    x, y, w, h = cv2.boundingRect(c)
    if w>40:
        cx, cy = x + w / 2, y + h/ 2
        cx = np.round(cx).astype("int")
        cy = np.round(cy).astype("int")
        center=np.round((w)/2).astype("int")
        cv2.circle(output_img, (cx,cy), center , [0, 255, 0], 2)
        cv2.circle(output_img, (cx, cy), 2, [255, 0, 0], 2)
        i+=1

print(i)

cv2.imshow("images", np.hstack([image,output_img]))
cv2.waitKey(0)

tk = tkinter.Tk()
frame = tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)
label = tkinter.Label(frame, text="count of ripe fruit= "+str(i))
label.pack(fill=X, expand=1)
pathlabel = tkinter.Label(frame)
button = tkinter.Button(frame,text="exit",command=tk.destroy)
button.pack(side=BOTTOM)
tk.mainloop()
