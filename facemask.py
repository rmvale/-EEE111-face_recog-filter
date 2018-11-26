import cv2
from PIL import Image, ImageDraw
import numpy
from imutils import face_utils, translate, rotate, resize

def getangle(face_landmarks): #angle used for Specs and Hair tilting
    leftEye = numpy.array(face_landmarks['left_eye'])
    rightEye = numpy.array(face_landmarks['right_eye'])

    # compute the center of mass for each eye
    leftEyeCenter = leftEye.mean(axis=0).astype("int")
    rightEyeCenter = rightEye.mean(axis=0).astype("int")

    # compute the angle between the eye centroids
    dY = leftEyeCenter[1] - rightEyeCenter[1]
    dX = leftEyeCenter[0] - rightEyeCenter[0]
    angle = numpy.rad2deg(numpy.arctan2(dY, dX))

    # returns angle value
    return angle


class Specs:
    def __init__(self, image):
        self.image = image
    
    def apply(self, face_landmarks, angle, img):
        mask = self.image
        
        #sets ideal width and length [Specs is one eye]
        mask_width = (face_landmarks['nose_bridge'][0][0]) - (face_landmarks['chin'][0][0])
        mask_length = int(mask_width * mask.size[1] / mask.size[0])
        
        leftEye = numpy.array(face_landmarks['left_eye'])
        
        #processes the mask to ideal dimensions, etc.
        curr_mask = mask.resize((mask_width, mask_length), resample=Image.LANCZOS)
        curr_mask = curr_mask.rotate(angle, expand=True)
        curr_mask = curr_mask.transpose(Image.FLIP_TOP_BOTTOM)
        
        #sets the coordinates and pastes the mask to the image
        xcoor = (leftEye[0,0] - mask_width // 4) - 15
        ycoor = leftEye[0,1] - mask_width // 6
        img.paste(curr_mask, (xcoor, ycoor), curr_mask)

class Hair:
    def __init__(self, image):
        self.image = image

    def apply(self, face_landmarks, angle, img):
        mask = self.image

        #sets ideal length, width
        mask_width = ((face_landmarks['chin'][-1][0] ) - (face_landmarks['chin'][0][0])) * 2
        mask_length = int(mask_width * mask.size[1] / mask.size[0])
        
        #processes the mask to ideal dimensions, etc.
        curr_mask = mask.resize((mask_width, mask_length), resample=Image.LANCZOS)
        curr_mask = curr_mask.transpose(Image.FLIP_LEFT_RIGHT)
        curr_mask = curr_mask.rotate(angle, expand=True)
        curr_mask = curr_mask.transpose(Image.FLIP_TOP_BOTTOM)
        
        #sets coordinates and then pastes the mask to the image
        yhair = numpy.array(face_landmarks['chin'])[0][1] - mask_length
        xhair = numpy.array(face_landmarks['chin'])[0][0] - (mask_width // 4)
        img.paste(curr_mask, (xhair, yhair), curr_mask)



