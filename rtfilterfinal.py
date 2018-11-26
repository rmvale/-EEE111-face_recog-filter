import face_recognition
import cv2
from PIL import Image, ImageDraw
import numpy
from imutils import face_utils, translate, rotate, resize
from makeup import Makeup
from aura import Aura
from facemask import *

# Running face recognition on live video from your webcam WITH FILTERS!!!. Complicated,
# but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/2 resolution (display also at 1/2 resolution since rescaling it blurs the image)
#   2. Only detect faces in every other frame of video.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

#instantiates required objects
ssjhair = Hair(Image.open("sshair.png")) 
basehair = Hair(Image.open("basehair.png"))
scouter = Specs(Image.open("Scouter2.png"))
a1 = Aura(Image.open("aura3.png"))
a2 = Aura(Image.open("aura4.png"))
ssa1 = Aura(Image.open("basaura1.png"))
ssa2 = Aura(Image.open("basaura2.png"))
yellowmakeup = Makeup('yellow')

countaura = 1

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/2 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]


    face_landmarks_list = face_recognition.face_landmarks(rgb_small_frame)

    for face_landmarks in face_landmarks_list:
        pil_image = Image.fromarray(rgb_small_frame)
        d = ImageDraw.Draw(pil_image, 'RGBA')
        mouth_open = (face_landmarks['bottom_lip'][1][1] - face_landmarks['top_lip'][1][1]) >= 10
        
        angle = getangle(face_landmarks)

        if mouth_open: #checks if mouth is open

        # Make the eyebrows into a supersaiyan hue
            yellowmakeup.apply(d, face_landmarks, 'left_eyebrow')
            yellowmakeup.apply(d, face_landmarks, 'right_eyebrow')

        # Sparkle the eyes
            yellowmakeup.apply(d, face_landmarks, 'left_eye')
            yellowmakeup.apply(d, face_landmarks, 'right_eye')

        # overlays specs and hair
            scouter.apply(face_landmarks, angle, pil_image)
            ssjhair.apply(face_landmarks, angle, pil_image)

        # alternating auras for the illusion of motion 
            if countaura % 2 == 0:
                ssa2.apply(pil_image)
                a2.apply(pil_image)
            else:
                ssa1.apply(pil_image)
                a1.apply(pil_image)
            countaura +=1

        else: #else, just overlays scouter and another hair
            scouter.apply(face_landmarks, angle, pil_image)
            basehair.apply(face_landmarks, angle, pil_image)

        small_frame = cv2.cvtColor(numpy.asarray(pil_image), cv2.COLOR_RGB2BGR)
        
    # realtime feed the scaled frame [if no face] or the filtered image [if face detected]
    cv2.imshow('SSJ', small_frame)


    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
