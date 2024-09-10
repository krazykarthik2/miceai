
# How It Works.
## Using your Hand as Cursor
- Figure out the index finger's position in the output,
    - Make the index finger's position be the cursor's position
    - Smooth the transition when needed
- Don't accept 2 hands at a time

## Figuring out your hand and fingers
- I used mediapipe and mp.hands to figure out the points in hands with models that are in built in media pipe library
- Then I presented them in a window for debugging
- Next Figure out the distance between index finger's farthest point and middle finger's farthest point, and ring finger's farthest point
## Click
- When the distance between index finger's farthest and middle finger's farthest is lesser than threshold,
- Register a click while not moving the cursor
## Dragging
- When the both index finger and middle finger and ring finger are open , then register a mouse clicking and
- while also allowing the cursor to move by the position of your index finger
## Tuning
- While this has a lot of shaking, I improved smoothing in the program
- Also, a decent amount of padding is given such that it is easy to move the cursor around while being in the middle of the screen allowing smoother interaction

# Personal Note
- This project was originally developed to be used with esp32cam, but now is fully software supporting
- Please raise issue if you have any doubts.
- Thank you.

 
# Dependencies

- numpy
- opencv-python
- pyqt5
- tkinter
- pillow
- mediapipe
- pyautogui

# design resources
go here

https://www.figma.com/design/a7b0OaPBKdhMmETYvGsCz2/MICEAI?node-id=0%3A1&t=fDm7Rsf9RtQEF2tr-1
write the python

create a init.bat file

convert init.bat file to init.exe file using [advbattoexeconverter.exe](https://www.battoexeconverter.com/downloads/advbattoexeconverter.exe)
