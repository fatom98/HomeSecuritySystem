# import all the library
import cv2, time
import numpy as np
from os import listdir, makedirs
from os.path import isfile, join, exists

class Recognise:
    
    def __init__(self):
        self.faceClassifier = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')

    def create(self, name):

        if not exists(f"faces/{name}"):
            makedirs(f"faces/{name}")
        # crop the image into 20 by 20 px and change it to B&W
        def face_extractor(img):
            # Function detects faces and returns the cropped face
            # If no face detected, it returns the input image
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.faceClassifier.detectMultiScale(gray, 1.3, 5)
            if faces == ():
                return None

            croppedFace = None
            # Crop all faces found
            for (x, y, w, h) in faces:
                croppedFace = img[y:y + h, x:x + w]

            return croppedFace

        num = 1
        cap = cv2.VideoCapture(0)
        # count the total number of faces
        count = 0
        print("Start Capturing the input Data Set  ")
        # Collect 100 samples of your face from webcam input
        while True:
            ret, frame = cap.read()
            # condition to check if face is in the frame or not
            if face_extractor(frame) is not None:
                count += 1
                face = cv2.resize(face_extractor(frame), (200, 200))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                # Save file in specified directory with unique name
                file_name_path = f'./faces/{name}/' + str(count) + '.jpg'
                cv2.imwrite(file_name_path, face)

                # Put count on images and display live count
                cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Face Cropper', face)

            else:
                print("Face not found")
                pass

            # checks if ech user 100 images is captured
            if (count % 100) == 0 and count != num * 100 and count != 0:
                print("Place the new user Signature")
                cv2.waitKey()

            # checks if total images are captured
            if cv2.waitKey(1) == 13 or count == num * 100:  # 13 is the Enter Key
                break

        # closes all windows
        cap.release()
        cv2.destroyAllWindows()
        print("Collecting Samples Complete")
    
    def train(self, name):
    
        try:
            # Get the training data we previously made
            data_path = f'faces/{name}/'
            onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    
            # Create arrays for training data and labels
            Training_Data, Labels = [], []
    
            # Open training images in our data path
            # Create a numpy array for training data
            for i, files in enumerate(onlyfiles):
                image_path = data_path + onlyfiles[i]
                images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                Training_Data.append(np.asarray(images, dtype=np.uint8))
                Labels.append(i)
    
            # Create a numpy array for both training data and labels
            Labels = np.asarray(Labels, dtype=np.int32)
    
            # Initialize facial recognizer
            self.model = cv2.face.LBPHFaceRecognizer_create()
    
            # Let's train our model
            self.model.train(np.asarray(Training_Data), np.asarray(Labels))
            print("Model trained successfully")
    
        except AttributeError:
            print("Please uninstall opencv-python and install opencv-contrib-python instead")
        self.test()

    def test(self):

        def face_detector(img):
            # Convert image to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.faceClassifier.detectMultiScale(gray, 1.3, 5)
            if faces == ():
                return img, []
    
            roi = None
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
                roi = img[y:y + h, x:x + w]
                roi = cv2.resize(roi, (200, 200))
            return img, roi
    
    
        # Open Webcam
        cap = cv2.VideoCapture(0)
    
        while True:
            # reads images from webcam
            ret, frame = cap.read()
    
            image, face = face_detector(frame)

            # noinspection PyBroadException
            try:
                # converts it into required format
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    
                # Pass face to prediction model
                # "results" comprises of a tuple containing the label and the success value
                results = self.model.predict(face)
                
                display_string = None
                success = None

                if results[1] < 500:
                    success = int(100 * (1 - (results[1]) / 400)) + 15
                    display_string = str(success) + '% success Authorised User'
    
                cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 120, 150), 2)
                # checks for matching characteristics

                if success > 95:
                    cv2.imshow('Face Recognition', image)
                    time.sleep(1)
                    cap.release()
                    cv2.destroyAllWindows()
                    return "unlocked"
                else:
                    cv2.imshow('Face Recognition', image)
    
            # if no face is present in the frame
            except:
                cv2.putText(image, "No Face Found", (220, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('Face Recognition', image)
                pass
    
            if cv2.waitKey(1) == 13:  # 13 is the Enter Key
                break
        # exit()
        cap.release()
        cv2.destroyAllWindows()