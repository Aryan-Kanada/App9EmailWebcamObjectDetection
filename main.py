import cv2
import time
from emailing import send_email
import glob
import os
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)
first_frame = None
status_list = []
count = 1
no_object_start_time = None

def clean_folder():
    print("start cl")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
        print("end cle")

while True:
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_blur = cv2.GaussianBlur(gray_frame, (13, 13), 0)

    if first_frame is None:
        first_frame = gray_frame_blur
    delta_frame = cv2.absdiff(first_frame, gray_frame_blur)
    thresh_frame = cv2.threshold(delta_frame, 30,255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]


    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:

        email_thread = Thread(target=send_email, args=(image_with_object, ))
        email_thread.daemon = True

        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        email_thread.start()

        no_object_start_time = time.time()

    if no_object_start_time:
        if time.time() - no_object_start_time >= 20:
            clean_thread.start()
            break

    print(status_list)
    cv2.imshow("My Video", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        clean_thread.start()
        break

video.release()



