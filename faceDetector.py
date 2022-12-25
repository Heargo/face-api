
from PIL import Image, ImageDraw
import face_recognition


def checkImage(image_to_check, face_to_seach):
    # Load the jpg file into a numpy array
    image = face_recognition.load_image_file(image_to_check)

    picture_of_me = face_recognition.load_image_file(face_to_seach)
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

    # Find all facial features in all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)
    print("I found "+str(len(face_landmarks_list))+" face(s) in this "+image_to_check)
    unknown_faces_encoding = face_recognition.face_encodings(image)

    n=0
    myFaceIndex = -1
    for face_encoding in unknown_faces_encoding:
        results = face_recognition.compare_faces([my_face_encoding], face_encoding)
        if results[0] == True:
            print("I'm in the picture, face number", n)
            myFaceIndex = n
        n = n + 1

    # Create a PIL imagedraw object so we can draw on the picture
    if myFaceIndex !=-1:
        pil_image = Image.fromarray(image)
        d = ImageDraw.Draw(pil_image)

        for face_landmarks in face_landmarks_list:

            # Let's trace out each facial feature in the image with a line!
            for facial_feature in face_landmarks.keys():
                #change to red if it's me
                if face_landmarks == face_landmarks_list[myFaceIndex]:
                    d.line(face_landmarks[facial_feature], fill=(255, 0, 0), width=5)
                else:
                    d.line(face_landmarks[facial_feature], width=5)

        # Show the picture
        pil_image.show()

    return myFaceIndex!=-1