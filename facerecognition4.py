import face_recognition
import glob

known_faces_encodings = dict()
test_image_encodings = []
quantity_faces = []

for i in glob.glob("/home/alexandr/PycharmProjects/chatbot/base_of_photos/*.jpg"):
    photo = face_recognition.load_image_file(i)
    #print(face_recognition.face_encodings(photo))
    if not face_recognition.face_encodings(photo) == []:
        known_faces_encodings[i] = face_recognition.face_encodings(photo)[0]

for i in glob.glob("/home/alexandr/PycharmProjects/chatbot/photos/*.jpg"):
    test_image = face_recognition.load_image_file(i)
    test_image_locations = face_recognition.face_locations(test_image)
    #print(test_image_encodings)
    if not test_image_locations == []:
        test_image_encoding = face_recognition.face_encodings(test_image, test_image_locations)[0]
        test_image_encodings.append(test_image_encoding)
        quantity_faces.append(test_image_locations)




