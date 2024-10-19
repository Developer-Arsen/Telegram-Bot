import cv2 as cv

def checkIsSelfie(path):
    face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    img = cv.imread(path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 0:
        return False
    
    return True