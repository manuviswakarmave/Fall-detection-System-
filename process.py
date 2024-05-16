import re
import cv2

email_con = "^[a-z]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$"
phone_con = "(0|91)?[-\s]?[6-9][0-9]{9}"


def check_whole(email, phone):    
    if re.search(email_con, email):
        print("Right")
    else:
        print("Wrong")

    if re.search(phone_con, phone):
        print("Right")
    else:
        print("Wrong")

def check(email):    
  flag = 0  
  if re.search(email_con, email):
    print("Right")
    flag = 1
  else:
    print("Wrong")
    flag = 0
    
  return flag

def on_camera():
    camera_on = True
    cam = cv2.VideoCapture(0)
    
    while camera_on:
            ret, img =cam.read()
            cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
            cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cv2.imshow("webcam",img)
            if not ret:
                break
            k=cv2.waitKey(10)
            if k%256 == 27:
                print("Closing...")
                break
            elif k%256 == 32:

                camera_on = False

    cam.release()
    cv2.destroyAllWindows()