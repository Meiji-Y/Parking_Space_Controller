import cv2
import pickle

# Parking space rectangular sizes.
# You can change this variables for your parking space size.
width, height = 107, 48

#This part loads spaces from file
try:
    with open('CarParkPosition', 'rb') as f:
        positionList = pickle.load(f)
except:
    positionList = []

# This function creates rectangular for parking spaces when right-clicked. When left click, it deletes the created area.
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        positionList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, position in enumerate(positionList):
            x1, y1 = position
            if x1 < x < x1 + width and y1 < y < y1 + height:
                positionList.pop(i)

    #This part saves spaces into the file
    with open('CarParkPosition', 'wb') as f:
        pickle.dump(positionList, f)


while True:
    img = cv2.imread('carParkImg.png')
    for position in positionList:
        cv2.rectangle(img, position, (position[0] + width, position[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)