import cv2
import mediapipe as mp
import time
import math
from the_utils import distance,is_near
print('global init')


class handDetector():
    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, 
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
    img = None
    def findHands(self, img, draw=True):
        self.img = img # for further use may delete later
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
 
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)
 
        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            
            
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax
            self.xmin, self.ymin, self.xmax, self.ymax = xmin, ymin, xmax, ymax
            if draw:
                for id, lm in enumerate(myHand.landmark):
                    cv2.circle(img, (xList[id], yList[id]), (min(xmax - xmin, ymax - ymin)//20), (255, 0, 100), cv2.FILLED)
            
 
            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),(0, 255, 0), 2)
 
        return self.lmList, bbox

    def findAngle(self, p1, p2, p3,id, draw=True):
        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
 
        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360
        # print(angle)
 
        # Draw
        if draw:
            __radius = (min(self.xmax - self.xmin,self.ymax - self.ymin)//20)
            cv2.line(self.img, (x1, y1), (x2, y2), (150,150,150), 3)
            cv2.line(self.img, (x3, y3), (x2, y2), (150,150,150), 3)
            cv2.circle(self.img, (x1, y1), __radius, (0, 0, 255), cv2.FILLED)
            cv2.circle(self.img, (x1, y1), int(__radius*1.5), (0, 0, 255), 2)
            cv2.circle(self.img, (x2, y2), __radius, (0, 0, 255), cv2.FILLED)
            cv2.circle(self.img, (x2, y2), int(__radius*1.5), (0, 0, 255), 2)
            cv2.circle(self.img, (x3, y3), __radius, (0, 0, 255), cv2.FILLED)
            cv2.circle(self.img, (x3, y3), int(__radius*1.5), (0, 0, 255), 2)
            cv2.putText(self.img, str(int(angle)), (x2 - __radius*5, y2 + __radius*5),
                        cv2.FONT_HERSHEY_PLAIN, (__radius/5), (0, 0, 255), 2)
            cv2.putText(self.img, str(int(angle)), (20 + id*50,20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        return angle
    
    def fingersUp(self):
        fingers = []
        # Thumb
        if not len(self.lmList)<1:
            try:
                if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        
                # Fingers
                for id in range(1, 5):
                    
                    # find out the angle between id and id-3 and 0 at id-3 
                    angle = self.findAngle(self.tipIds[id],self.tipIds[id]-3,0,id)
                    obtuse_angle = angle > 130
                    if obtuse_angle:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                        
            except Exception as e:
                print('exception')
            # totalFingers = fingers.count(1)
    
        return fingers

    def findDistance(self, p1, p2, img, draw=True,r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
 
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 100), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 100), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 100), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)
 
        return length, img, [x1, y1, x2, y2, cx, cy]

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    print('capturing video')
    detector = handDetector()
    while True:
        
        success, img = cap.read()
        
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
 
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        fingers = detector.fingersUp()
 
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
 
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if(key == 27):
            break
 
 
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('exception')
        print(e)