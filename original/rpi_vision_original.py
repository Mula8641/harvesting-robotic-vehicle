import cv2
import numpy as np
import time
import requests


# Initialize camera
cap = cv2.VideoCapture(0)

url = "http://192.168.4.1/"

width = 255
height = 255
dis = 40
driveDist = 5
pickDist = 5
delayTime = 1

# Define the focal length of the camera in pixels
focal_length = 520

# set video size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Set up the range of red color in HSV
lower_red = np.array([0, 47, 40])
upper_red = np.array([14, 255, 255])

# Initialize previous position
prev_x = 0
a = 0
b = 50

def adjust_brightness(image, value):
    # Convert the image to float32 for arithmetic operations
    image = image.astype(np.float32)

    # Add the brightness value to all pixel values
    adjusted_image = image + value

    # Clip the pixel values to ensure they remain within the valid range (0-255)
    adjusted_image = np.clip(adjusted_image, 0, 255)

    # Convert the image back to uint8 format
    adjusted_image = adjusted_image.astype(np.uint8)

    return adjusted_image

while True:
    # Read frame from camera
    ret, frame = cap.read()
    
    #invert frame
    frame = cv2.flip(frame, 0)
    
    frame = adjust_brightness(frame, b)

    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    

    # Apply color thresholding to get only red color
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Apply morphological operations to remove noise
    '''kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)'''
    imgResult = cv2.bitwise_and(frame,frame,mask=mask)

    # Find contours in the mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contour was found
    if len(contours) > 0:
        # Find the largest contour
        c = max(contours, key=cv2.contourArea)

        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(c)

        # Draw the rectangle around the contour
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calculate the x-coordinate of the center of the rectangle
        center_x = x + w/2
        center_y = y + h/2

        # Calculate the distance of the object from the camera
        object_width = w
        distance = (4 * focal_length) / object_width


        # Draw a green rectangle around the object
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "{:.2f} cm".format(distance), (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        #if distance > driveDist:
        #drive the robot
        if center_x > (width/2)+dis:
            if a == 0:
                r = requests.get(url+"?State=l")
                print("right")
                a = 1
                
        elif center_x < (width/2)-dis:
            if a == 0:
                r = requests.get(url+"?State=r")
                print("left")
                a = 1
       
        else:
            if a == 1:
                r = requests.get(url+"?State=s")
                print("center")
                a = 0


            # Send the y-coordinate to Arduino
            if center_y > (height/2)+dis:
                if a == 0:
                    r = requests.get(url+"?State=f")
                    print("downf",center_y)
                    a = 1
                
            elif center_y < (height/2)-dis:
                if a == 0:
                    r = requests.get(url+"?State=f")
                    print("up",center_y)
                    a = 1
                
            else:
                if a == 1:
                    print("center picking",center_y)
                    r = requests.get(url+"?State=sa")
                    a = 0
                           
    else:
        if a == 1:
            print("stop")
            r = requests.get(url+"?State=s")
            a = 0
        

    # Show the frame
    cv2.imshow('Frame', frame)

    # Exit if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
