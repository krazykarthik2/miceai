import numpy as np
import track_hand as htm
import time
import pyautogui
import cv2
import urllib

wCam, hCam = 1280, 720
frameR = 200
smoothening = 3.4

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()
isMouseDown = False


def do_the_thing(url):
    global wCam,hCam,frameR,smoothening,cap,detector,wScr,hScr,isMouseDown,pTime,clocX,clocY,plocX,plocY
    while True:
        fingers = [0, 0, 0, 0, 0]
        # success, img = cap.read()


        img_resp=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        img=cv2.imdecode(imgnp,-1)
        


        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        try:
            if fingers[1] == 1 and fingers[2] == 0:
                if isMouseDown:
                    pyautogui.mouseUp()
                    isMouseDown = False 
                

                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening


                pyautogui.moveTo(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY
                
            if fingers[1] == 1 and fingers[2] == 1:
                length, img, lineInfo = detector.findDistance(8, 12, img)
                if length < 50:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    if not isMouseDown:
                        pyautogui.mouseDown()
                        isMouseDown = True
                
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening


                pyautogui.moveTo(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY

                    
            else:
                if isMouseDown:
                    pyautogui.mouseUp() 
                    isMouseDown = False 
                pass #there is more distance between the fingers 1 and 2 
        except:
            pass
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, "miceai", (20, 30), cv2.FONT_HERSHEY_PLAIN, 1.2, (200, 200, 200), 3)
        cv2.putText(img, str(int(fps))+'fps', (20, 50), cv2.FONT_HERSHEY_PLAIN, 1.2, (200, 200, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
if __name__=='__main__':
    do_the_thing()
    