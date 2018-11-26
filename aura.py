import cv2
from PIL import Image, ImageDraw
import numpy
from imutils import face_utils, translate, rotate, resize

#class takes in an image, applies that image to another image
class Aura:
    def __init__(self, image):
        self.image = image
    
    def apply(self, img):
        mask = self.image
        mask = mask.resize((img.size[0], img.size[1]), resample=Image.LANCZOS)
        img.paste(mask, (0,0), mask)

