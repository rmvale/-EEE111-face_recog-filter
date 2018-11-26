#the class takes in an Image object

from PIL import Image, ImageDraw

class Makeup:
    def __init__(self, color):
        self.color = color.lower()
    
    def apply(self, img, face_landmarks, feature):
        if self.color == 'yellow': #different RGBA codes for each color

            if feature.lower() == 'left_eyebrow' or 'right_eyebrow':
                #fills the brow outline with yellow
                img.polygon(face_landmarks[feature.lower()], fill=(255, 255, 0, 30))
                img.line(face_landmarks[feature.lower()], fill=(255, 255, 0, 50), width=5)

            elif feature.lower() == 'left_eye' or 'right_eye':
                #fills the eye outline with yelloe
                img.polygon(face_landmarks[feature.lower()], fill=(255, 255, 0, 30))
                img.line(face_landmarks[feature.lower()] + [face_landmarks[feature.lower()][0]], fill=(255, 255, 0, 50), width=6)
            
            else:
                pass #the current program [filter] will only be applying "makeup" to brows and eyes
        else:
            pass    #the current program [filter] will only be using yellow
                
                
            
    
