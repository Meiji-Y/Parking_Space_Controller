import cv2
import pickle
import cvzone
import numpy as np

# Your video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('CarParkPosition', 'rb') as f:
    posList = pickle.load(f)

# Parking space rectangular sizes.
# You can change this variables for your parking space size.
width, height = 107, 48

#This function calculates optimum count number for full parking spaces
def findFullParkSpaceCount(imgPro):
    countList=[]
    for pos in posList:
        x, y = pos
        
        # seperate parking spaces for checking
        imgCrop = imgPro[y:y + height, x:x + width]
        
        # count non zero pixels for detecting parking spaces, free or not
        count = cv2.countNonZero(imgCrop)
        countList.append(count)
        
    sorted_list = sorted(countList)

    # Calculate differences between consecutive elements
    differences = [sorted_list[i+1] - sorted_list[i] for i in range(len(sorted_list) - 1)]

    max_diff = max(differences)
    max_diff_index = differences.index(max_diff)

    fullParkSpaceCount = sorted_list[max_diff_index+1]
    return fullParkSpaceCount
    
#This function checks parking space free or not and counts empty spaces in parking lot
def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        FullParkSpaceCount=findFullParkSpaceCount(imgPro)
        
        x, y = pos
        
        # seperate parking spaces for checking
        imgCrop = imgPro[y:y + height, x:x + width]
        
        # count non zero pixels for detecting parking spaces, free or not
        count = cv2.countNonZero(imgCrop)
        
        if count < FullParkSpaceCount:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
            text="Free"
        else:
            color = (0, 0, 255)
            thickness = 2
            text="Full"

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(text), (x, y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                           thickness=5, offset=20, colorR=(0,200,0))
    
    
while True:
    
    #if statement using for restarting video 
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    
    cv2.imshow("Image", img)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThres", imgMedian)
    cv2.waitKey(10)