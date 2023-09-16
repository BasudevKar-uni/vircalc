import cv2
from cvzone.HandTrackingModule import HandDetector


class Button:
    def __init__(self,pos,width,height,value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self,img):
        # button
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (225,225,225), cv2.FILLED)
        cv2.rectangle(img, self.pos,(self.pos[0] + self.width, self.pos[1] + self.height),
                      (50,50,50),3)

        cv2.putText(img, self.value, (self.pos[0] + 20, self.pos[1] + 30),cv2.FONT_HERSHEY_PLAIN,
                    1,(50,50,50),1)

    def checkclick(self,x,y):
        if self.pos[0]<x<self.pos[0] + self.width and \
                self.pos[1]<y<self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (255,255,255), cv2.FILLED)
            cv2.rectangle(img, self.pos,(self.pos[0] + self.width, self.pos[1] + self.height),
                          (50,50,50),3)
            cv2.putText(img, self.value, (self.pos[0] + 7, self.pos[1] + 45),cv2.FONT_HERSHEY_PLAIN,
                        3,(0,0,0),3)
            return True
        else:
            return False


# webcam
cap = cv2.VideoCapture(0)
cap.set(3, 480)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)
# creating button
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['/', '0', '.', '='],]

buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x*50 + 300
        ypos = y*50 +115
        buttonList.append(Button((xpos,ypos), 50, 50, buttonListValues[y][x]))

# variable
myEquation = ''
delayCounter = 0

# loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # detect hand
    hands, img = detector.findHands(img, flipType=False)

    # draw button
    cv2.rectangle(img, (300,60), (300 + 200, 70 + 50),
                  (225,225,225), cv2.FILLED)
    cv2.rectangle(img, (300,60), (300 + 200, 70 + 50),
                  (50,50,50),2)
    for button in buttonList:
        button.draw(img)

    # check for hand
    if hands:
        # Get the landmarks of the first hand (you can change this to the second hand if needed)
        hand1 = hands[0]

        # Get the landmarks of the index and middle fingers
        index_finger = hand1["lmList"][8][:2]  # Index finger tip
        middle_finger = hand1["lmList"][12][:2]  # Middle finger tip

        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(index_finger, middle_finger, img)
        x,y = index_finger
        if length<50:
            for i, button in enumerate(buttonList):
                if button.checkclick(x,y) and delayCounter == 0:
                    myValue = buttonListValues[int(i % 4)][int(i/4)]
                    if myValue == '=':
                        myEquation = str(eval(myEquation))
                    else:
                        myEquation += myValue
                    delayCounter = 1

    # Avoid Duplicates
    if delayCounter != 0:
        delayCounter +=1
        if delayCounter >10:
            delayCounter = 0

    # display result
    cv2.putText(img, myEquation, (300, 110),cv2.FONT_HERSHEY_PLAIN,
                2,(50,50,50),2)

    # display image
    cv2.imshow("image", img)
    key = cv2.waitKey(1)
    if key == ord('c'):
        myEquation = ''
    elif key == ord('b'):
        myEquation = myEquation[:-1]
    elif key == 27:  # 27 is the ASCII code for the 'Esc' key
        break
        cap.release()
        cv2.destroyAllWindows()
