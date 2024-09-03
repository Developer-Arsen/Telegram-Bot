# import cv2 as cv
# import face_recognition

# def checkIsSelfie(path):
#     img = cv.imread(path)
#     test = cv.cvtColor(img, cv.COLOR_BGR2RGB)
#     face_locations = face_recognition.face_locations(test)

#     if not face_locations:
#         return False
    
#     # height, width, _ = img.shape
#     # image_center = (width / 2, height / 2)

#     # for face in face_locations:
#     #     top, right, bottom, left = face
#     #     face_center = ((left + right) / 2, (top + bottom) / 2)

#     #     if abs(face_center[0] - image_center[0]) < width * 0.2 and abs(face_center[1] - image_center[1]) < height * 0.2:
#     #         return True
#     return True



import cv2 as cv

def checkIsSelfie(path):
    face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    img = cv.imread(path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) == 0:
        return False
    
    # check if image want to be in center
    # height, width, _ = img.shape
    # image_center = (width / 2, height / 2)
    
    # for (x, y, w, h) in faces:
    #     face_center = (x + w / 2, y + h / 2)
        
    #     if abs(face_center[0] - image_center[0]) < width * 0.2 and abs(face_center[1] - image_center[1]) < height * 0.2:
    #         return True
    
    return True