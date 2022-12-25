from faceDetector import checkImage
from instaLoader import GetInstagramProfile
import os
#only for first time/ or if you want to change user/ reload session. Read the session name print in the console.
#updateSession()

cls = GetInstagramProfile()
cls.L.load_session_from_file("sessionName")

#try on accountWithPostOnMe
cls.download_post_since_date("accountWithPostOnMe",[2022, 9, 1])

myface ="me.jpg"

#for each picture in the folder downloads check if there is my face in it
listOfFiles = []
for filename in os.listdir("downloads"):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        if checkImage("downloads/"+filename,myface):
            print("found my face in "+filename)
            listOfFiles.append("downloads/"+filename)
    else:
        continue

print("found in total "+str(len(listOfFiles))+" pictures with my face in it")
print(listOfFiles)

