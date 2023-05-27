from deepface import DeepFace 
import cv2
from faceDetector import checkImage
import time


# loader = GetInstagramProfile()
# loader.get_users_followers("heargo_82")
def deepCheck(img1_path,img2_path):
    result = DeepFace.verify(img1_path = "me.jpg", img2_path = "downloads/tes1/IMG-20221204-WA0020.jpg")
    print(result)
    #show image with a bounding box around the face
    img = cv2.imread("downloads/tes1/IMG-20221204-WA0020.jpg")
    area = result["facial_areas"]
    #cv2.rectangle(img, (area["img2"]["x"], area["img2"]["y"]), (area["img2"]["x"] + area["img2"]["w"], area["img2"]["y"] + area["img2"]["h"]), (0, 155, 255), 2)
    #cv2.imshow("img",img)
    #cv2.waitKey(0)

#compare the speed of the two methods
#deepCheck("me.jpg","downloads/tes1/IMG-20221204-WA0020.jpg")
#checkImage("downloads/tes1/IMG-20221204-WA0020.jpg","me.jpg")
start_time = time.time()
deepCheck("me.jpg","downloads/tes1/IMG-20221204-WA0020.jpg")
print("--- %s seconds for deepface ---" % (time.time() - start_time))
start_time = time.time()
checkImage("downloads/tes1/IMG-20221204-WA0020.jpg","me.jpg")
print("--- %s seconds for face_recognition ---" % (time.time() - start_time))
