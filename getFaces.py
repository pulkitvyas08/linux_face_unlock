from os import listdir, system
from os.path import isfile, join

import numpy as np
from face_recognition import face_encodings, face_locations

from cv2 import ( 
    destroyAllWindows,
    imshow, 
    resize,
    VideoCapture,
    waitKey,
)

def getFaces(training=False):
    
    path = '/lib/Auth/RecFace/roots/'
    if training:
        system(f"sudo chattr -R -i {path}")
        system(f"sudo chmod -R ugo+rw {path}")
        print("There shold be only one person in frount of the camera!")
        print("It will only save the model if there is exactly one face.\n Press [ENTER] to proceed: ")
        input()
    saved=False
    cap = VideoCapture(0)
    loop_count = 0
    while not saved:
        loop_count += 1
        _, img = cap.read()
        
        small_frame = resize(img, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locs = face_locations(rgb_small_frame)
        face_code = face_encodings(rgb_small_frame, face_locs)
        
        if len(face_locs) == 1:
            if not training:
                return face_code
            try:
                root_models = [f for f in listdir(path) if isfile(join(path, f))]
                a = len(root_models)
            except:
                a = 0
            face_code = np.asarray(face_code)
            np.save(f"{path}root-{a}.npy", face_code)
            system(f"sudo chmod -R ugo-w {path}")
            system(f"sudo chattr -R +i {path}")
            saved = True

        else:
            if training:
                imshow("Image", img)

            if len(face_code) > 1:
                if not training:
                    return face_code
                cap.release()
                destroyAllWindows()
                raise Exception("More than one faces found!")
            else:
                if loop_count > 200:
                    cap.release()
                    destroyAllWindows()
                    raise Exception("No faces detected.")
        
        if waitKey(1) & 0xFF == ord('q'):
            cap.release()
            destroyAllWindows()        
            
    cap.release()
    destroyAllWindows()
