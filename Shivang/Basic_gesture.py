import cv2
import time
import pickle
import mediapipe as mp
import math
import time
class mpHands:
    import mediapipe as mp
    def __init__(self,maxHands=2,tol1=.5,tol2=.5):
        self.hands=self.mp.solutions.hands.Hands(False,maxHands,1,tol1,tol2)
    def Marks(self,frame):
        myHands=[]
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.hands.process(frameRGB)
        if results.multi_hand_landmarks != None:
            for handLandMarks in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(frame, landmark_list = handLandMarks,connections = mp.solutions.hands.HAND_CONNECTIONS)
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands

def findDistance(handData):
    l=[]
    palmSize=math.pow((handData[0][0]-handData[9][0])**2+(handData[0][1]-handData[9][1])**2,0.5)
    for i in handData:
        temp=[]
        for j in handData:
            distance = (math.pow((i[0]-j[0])**2+(i[1]-j[1])**2,0.5))/palmSize
            temp.append(distance)
        l.append(temp)
    return l

def findError(gestureMatrix,unknownMatrix,keypoints):
    error=0
    for row in keypoints:
        for column in keypoints:
            error = error + abs(gestureMatrix[row][column]-unknownMatrix[row][column])
            # print(error)
    return error

def findGesture(unknownGesture,knownGestures,keypoints,gestnames,tol):
    errorArray=[]
    for i in range(len(gestnames)):
        error = findError(knownGestures[i],unknownGesture,keypoints)
        errorArray.append(error)
        errorMin = errorArray[0]
    
    minIndex=0

    for i in range (0,len(errorArray)):
        if errorArray[i]<errorMin:
            errorMin=errorArray[i]
            minIndex=i
    if errorMin<tol:
        gesture=gestNames[minIndex]
    if errorMin>=tol:
        gesture='Unknown'
    return gesture
def findDistancePoints(pt1,pt2):
    return math.pow((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2,0.5)

# time.sleep(5)

width=700
height=500
cam=cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 120)
# cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))
keypoints = [0,4,5,9,13,17,8,12,16,20]

train  = True

tol = 15

# (print("How Many gestures do you want ? "))
# time.sleep(3)
findHands=mpHands(1)
gestNames=[]

gestNames.append('fist')

# mpHand= mp.solutions.hands
mpDraw=mp.solutions.drawing_utils

boxcolor=(255,255,0)
boxthickness=3
check_list = []
with open("known.bin",'rb') as f:
    knowngestures = pickle.load(f)

start_time = time.time()
while True:
    ignore,  frame = cam.read()
    handData=findHands.Marks(frame)
    if handData!=[]:
        unknownGesture = findDistance(handData[0])
        myGesture = findGesture(unknownGesture,knowngestures,keypoints,gestNames,tol)
        if myGesture=="fist":
            check_list.append(1)
        else:
            check_list.append(0)

        if time.time()-start_time>6 and check_list:
            if sum(check_list)/len(check_list)>0.8:
                print("Welcome")
            else:
                print("get out")
            start_time = time.time()
            check_list=[]
        # for hand in handData:
            # cv2.rectangle(frame,(hand[17][0],hand[20][1]),(hand[1][0]+hand[4][0],hand[1][1]+hand[4][1]),boxcolor,boxthickness)
            # mpDraw.draw_landmarks(frame, landmark_list = hand,connections = mp.solutions.hands.HAND_CONNECTIONS)
        # error = findError(kownGesture,unknownGesture,keypoints)
        cv2.putText(frame,myGesture,(100,175),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),3)
    
    cv2.imshow('my WEBcam', frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()
