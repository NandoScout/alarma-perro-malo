import cv2
import numpy as np
import glob

img = cv2.imread('C:/Users/Administrador/Desktop/Camara de diputados/frames/imagen_0000000000.jpg')
height, width, layers = img.shape
size = (width,height)
out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 60, size)

for filename in glob.glob('C:/Users/Administrador/Desktop/Camara de diputados/frames/*.jpg'):
    img = cv2.imread(filename)
    out.write(img)



out.release()