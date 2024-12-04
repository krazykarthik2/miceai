import numpy as np
import track_hand as htm
import time
import pyautogui
import cv2
import urllib
from the_utils import are_points_near,distance

smoothening = 3.4

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

detector = htm.handDetector(maxHands=1)
wScr, hScr = pyautogui.size()
isMouseDown = False
isMinDesk  = False

running = True

print('global cpl')

pyautogui.FAILSAFE = False
def do_the_thing(url):
    global running
    global smoothening,cap,detector,wScr,hScr,pTime,clocX,clocY,plocX,plocY
    global isMouseDown,isMinDesk
    cap = cv2.VideoCapture(url)
    print('capturing video')
    wCam, hCam = int(cap.get(3))*2, int(cap.get(4))*2
    print(wCam, hCam)
    frameR =( min(wCam, hCam))//5
    while running:
        fingers = [0, 0, 0, 0, 0]
        success, img = cap.read()
        # scale img to 2 times
        img = cv2.resize(img, (wCam, hCam))
        img = cv2.flip(img, 1)
        
        img__ = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            fingertipsAt = [lmList[i][1:] for i in [4,8,12,16,20]]
        else:
            fingertipsAt=[]
        

        fingers = detector.fingersUp()
        
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        
        if len(fingers)==0:
            pass
        else: 
            try:
                if len(fingertipsAt)>0 and are_points_near(fingertipsAt,distance(lmList[5],lmList[0])): # to adjust the threshold
                    if isMouseDown:
                        pyautogui.mouseUp()
                        isMouseDown = False

                    if not isMinDesk:
                        pyautogui.hotkey('winleft','d')
                        isMinDesk=True
                else:
                    isMinDesk=False
                    if fingers==[1,0,0,0,0] : #thumb up all fingers down
                        if isMouseDown:
                            pyautogui.mouseUp()
                            isMouseDown = False 
                        pyautogui.keyDown("Ctrl")
                        pyautogui.press("c")
                        pyautogui.keyUp("Ctrl")
                        print("copied")
                    elif fingers==[1,0,0,0,1]:# thumb up ,last finger up
                        if isMouseDown:
                            pyautogui.mouseUp()
                            isMouseDown = False 
                        pyautogui.keyDown("Ctrl")
                        pyautogui.press("v")
                        pyautogui.keyUp("Ctrl")
                        print("pasted")
                    elif fingers[1:]==[1,0,0,0]:# index up, all down not considering thumb
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
                        
                    elif fingers[1:]==[1,1,0,0]:# index,mid up all down not considering thumb
                        length, img, lineInfo = detector.findDistance(8, 12, img)
                        if length < 100:
                            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                            if not isMouseDown:
                                pyautogui.mouseDown()
                                isMouseDown = True
                                print('..',end="")
                            print("down:",isMouseDown)

                    elif fingers[1:]==[1,1,1,1]:

                        length, img, lineInfo = detector.findDistance(8, 12, img)

                        if length < 100:
                            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                            if not isMouseDown:
                                pyautogui.mouseDown()
                                isMouseDown = True
                                print('..',end="")
                            print("down:",isMouseDown)

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
            except Exception as e:
                print(f'exception-{e}')
            except pyautogui.FailSafeException as e:
                print(f'at the corners')
        
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, "miceai", (10, 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (200, 200, 200), 3)
        cv2.putText(img, str(int(fps))+'fps', (20, 50), cv2.FONT_HERSHEY_PLAIN, 1.2, (200, 200, 0), 3)
        cv2.putText(img,str(fingers), (20, 70), cv2.FONT_HERSHEY_PLAIN, 1.2, (200, 200, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
