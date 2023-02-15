
# Quick demo that shows how to take photographs with the RoboMaster TT drones.
#   Notice that we are communicating with the drone directly. Of course, you'll
#   want to create a capability in your drone controller class.

from djitellopy import Tello
from datetime import datetime
import cv2
import time



# Thanks to estebanuri
# https://stackoverflow.com/questions/60674501/how-to-make-black-background-in-cv2-puttext-with-python-opencv
def cv2TextBoxWithBackground(img, text,
        font=cv2.FONT_HERSHEY_PLAIN,
        pos=(0, 0),
        font_scale=1,
        font_thickness=1,
        text_color=(30, 255, 205),
        text_color_bg=(48, 48, 48)):
    x, y = pos
    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_pos = (x, y + text_h + font_scale)
    box_pt1 = pos
    box_pt2 = (x + text_w+2, y + text_h+2)
    cv2.rectangle(img, box_pt1, box_pt2, text_color_bg, cv2.FILLED)
    cv2.putText(img, text, text_pos, font, font_scale, text_color, font_thickness)
    return img


# Connect to the drone and turn on the motors to cool down the drone

drone = Tello()
drone.connect()
drone.turn_motor_on()
print(f"Battery level is {drone.get_battery()}%")

# Turn on video stream and get the BackgroundFrameRead object

drone.streamon()
camera = drone.get_frame_read()

# Take the picture and show it in a cv2 window also save the picture to disk
# The video frame is actually a single frame from the video camera 

print('Taking picture in 3s... ', end='', flush=True)
time.sleep(1)
print('2s... ', end='', flush=True)
time.sleep(1)
print("1s... ")
time.sleep(1)
print("**********")
print("* CLICK! *")
print("**********")

image = camera.frame
text = datetime.now().strftime("%Y-%m-%d %H:%m.%S")
cv2TextBoxWithBackground(image, text)
cv2.imwrite("my_drone_photo.png", image)

# Sometimes the cv2 library does better if you add these very short waits

cv2.imshow("My Drone Photograph", image)
time.sleep(0.001)

# Wait for the user to close the image window or press the ESCAPE key
#   Start a while loop that finishes when the window is closed by clicking on
#   the X button. Every time through the loop, we wait 100 ms for the user to
#   press a key. If the key was ESCAPE then we quit. Otherwise we continue the
#   loop again. It's important to wait some time so that the CPU does not spin
#   around really fast in this loop and hog resources that would be better used
#   elsewhere.

print("Press the <ESC> key to quit")
value = 1.0
while value >= 1.0:
    value = cv2.getWindowProperty("My Drone Photograph", cv2.WND_PROP_VISIBLE)
    key_code = cv2.waitKey(100)
    if key_code & 0xFF == 27:
        break

print("Destroying all picture windows")
cv2.destroyAllWindows()

# Turn off the video stream and the drone

print("Closing connection")
time.sleep(1)
drone.streamoff()
drone.turn_motor_off()
print(f"Battery level is {drone.get_battery()}%")
drone.end()
print("Mission Complete")