import numpy as np
import cv2 as cv
import argparse

C_Thr = 0.43    # threshold for coherency
LowThr = 35     # threshold1 for orientation, it ranges from 0 to 180
HighThr = 57    # threshold2 for orientation, it ranges from 0 to 180
def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray
def blur(a):
    kernel = np.ones((52,52))
    kernel = kernel / np.sum(kernel)
    arraylist = []
    for y in range(3):
        temparray = np.copy(a)
        temparray = np.roll(temparray, y - 1, axis=0)
        for x in range(3):
            temparray_X = np.copy(temparray)
            temparray_X = np.roll(temparray_X, x - 1, axis=1)*kernel[y,x]
            arraylist.append(temparray_X)

    arraylist = np.array(arraylist)
    arraylist_sum = np.sum(arraylist, axis=0)
    return arraylist_sum
#a function for convolution operation
def naveenConvolve(img,kernel):
    row1total = img[0,1]*kernel[0,1] + img[0,2]*kernel[0,2] + img[0,0]*kernel[0,0]
    row2total = 0
    row3total = img[2,1]*kernel[2,1] + img[2,2]*kernel[2,2] + img[2,0]*kernel[2,0]
    return row1total + row2total + row3total

#a function for taking part of image to apply convolution between kernel and part of image
def takePartImage(inpimg,i,j):
    image = np.zeros((3,3))
    a = i
    b = j
    for k in range(0,3):
        b = j
        for l in range(0,3):
            image[k,l] = inpimg[a,b]
            b = b+1
        a = a +1
    return image

#a function for finding X gradient
def naveenSobelXgradient(inputimg):
    rows = len(inputimg)
    cols = len(inputimg[0])
    Gx = np.array(np.mat('1 0 -1; 2 0 -2; 1 0 -1'))
    outputimg = np.zeros((rows,cols))
    for i in range(0,rows-3):
         for j in range(0,cols-3):
             # retreve the part of image of 3 x 3 dimension from inputimage
             image  = takePartImage (inputimg, i, j)
             outputimg[i,j] = naveenConvolve(image,Gx)
    return outputimg

#a function for finding Y gradient
def naveenSobelYgradient(inputimg):
    rows = len(inputimg)
    cols = len(inputimg[0])
    #print(rows,cols)
    Gy = np.array(np.mat('1 2 1; 0 0 0; -1 -2 -1'))
    outputimg = np.zeros((rows,cols))
    for i in range(0,rows-3):
         for j in range(0,cols-3):
             # retreve the part of image of 3 x 3 dimension from inputimage
             image  = takePartImage (inputimg, i, j)
             outputimg[i,j] = naveenConvolve(image,Gy)
    return outputimg

#reading an image 
parser = argparse.ArgumentParser(description='Code for Anisotropic image segmentation tutorial.')
parser.add_argument('-i', '--input', help='Path to input image.', required=True)
args = parser.parse_args()
inputimg = rgb2gray(cv.imread(args.input)) # imgIn = cv.imread(args.input, cv.IMREAD_GRAYSCALE)
cv.imshow("Original", np.uint8(inputimg))
sobelimagex = naveenSobelXgradient((inputimg))
sobelimagey = naveenSobelYgradient((inputimg))
sobelimagex = np.float32(sobelimagex)
sobelimagey = np.float32(sobelimagey)
diffxy = [sobelimagex[i]*sobelimagey[i] for i in range(len(sobelimagex))]
diffxx = [sobelimagex[i]*sobelimagex[i] for i in range(len(sobelimagex))]
diffyy = [sobelimagey[i]*sobelimagey[i] for i in range(len(sobelimagey))]
# J11 = blur((diffxx))
# J22 = blur((diffyy))
# J12 = blur((diffxy))
# J11 = np.float32(J11)
# J22 = np.float32(J22)
# J12 = np.float32(J12)
w = 52
J11 = cv.boxFilter(np.float32(diffxx), cv.CV_32F, (w,w))
J22 = cv.boxFilter(np.float32(diffyy), cv.CV_32F, (w,w))
J12 = cv.boxFilter(np.float32(diffxy), cv.CV_32F, (w,w))

tmp1 = J11 + J22
tmp2 = J11 - J22
tmp2 = [tmp2[i]*tmp2[i] for i in range(len(tmp2))]
tmp3 = [J12[i]*J12[i] for i in range(len(J12))]
tmp4 = [tmp2[i] + 4.0*tmp3[i] for i in range(len(tmp2))]
tmp4 = np.sqrt(tmp4)
lambda1 = tmp1 + tmp4    # biggest eigenvalue
lambda2 = tmp1 - tmp4    # smallest eigenvalue

imgCoherencyOut=[((lambda1[i]-lambda2[i])/(lambda1[i]+lambda2[i])) for i in range(len(lambda1))]
imgOrientationOutDiff=[(J22[i]-J11[i]) for i in range(len(J22))]
imgOrientationOutMlt=[(2*J12[i]) for i in range(len(J12))]
imgOrientationDiv=[(imgOrientationOutDiff[i]/imgOrientationOutMlt[i]) for i in range(len(imgOrientationOutMlt))]
imgOrientationOut=np.arctan(imgOrientationDiv)
imgOrientationOut=imgOrientationOut*57.295779513
imgOrientationOut=0.5*imgOrientationOut

_, imgCoherencyBin = cv.threshold(np.float32(imgCoherencyOut), C_Thr, 255, cv.THRESH_BINARY)
_, imgOrientationBin = cv.threshold(np.float32(imgOrientationOut), LowThr, HighThr, cv.THRESH_BINARY)
imgBin = cv.bitwise_and(imgCoherencyBin, imgOrientationBin)
imgCoherency = cv.normalize(np.float32(imgCoherencyOut), None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
imgOrientation = cv.normalize(np.float32(imgOrientationOut), None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)

cv.imshow('result.jpg', np.uint8(0.5*(inputimg + imgBin)))
cv.imshow('Coherency.jpg', imgCoherency)
cv.imshow('Orientation.jpg', imgOrientation)
rows = len(inputimg)
cols = len(inputimg[0])

outputimg = np.zeros([rows, cols])

#finding the gradient magnitude by using the formula [abs(imgx) + abs(imgy)]
for i in range(0,rows):
    for j in range(0,cols):
        outputimg[i,j] = abs(sobelimagex[i, j]) + abs(sobelimagey[i, j])

#print(outputimg.size)
cv.imshow('sobel image',np.uint8(outputimg))
cv.waitKey(0)