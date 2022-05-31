import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 900)

detector = HandDetector(detectionCon = 0.8, maxHands=2)
cx, cy, w, h = 100, 100, 200, 200
lp = 0
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, _ = detector.findHands(img, flipType=False)
    
    #lmlist, _ = detector.findPosition(img)
    colorR = (255, 0, 255)
    
    if hands:
        hand = hands[0]
        lmList = hand['lmList'] # 21 landmark points
        bbox = hand['bbox'] #bounding box info x, y, w, h
        centerPoints = hand['center'] # center cx, cy
        handType = hand['type'] # gives which hand type, left or right

        cursor = lmList[8]
        #if detector.fingersUp(hand) == [0,0,0,0,0]:
        #    break
        if cx-w//2<cursor[0]<cx+w//2 and cy-h//2<cursor[1]<cy+h//2:
            colorR = (0,255,0)
            l,_ = detector.findDistance(lmList[8], lmList[12])
            #l,_ = detector.findDistance(lmList[8], lmList[6])
            
            if detector.fingersUp(hand) == [1,1,1,0,0]:
                if l < 40:
                    cx,cy=cursor
            elif detector.fingersUp(hand) == [0,1,0,0,0]:
                l,_ = detector.findDistance(lmList[8], lmList[4])
                
                siz = 5
                if lp>l or l < 20:
                    w-=siz
                    h-=siz
                elif lp<l or l > 130:
                    w+=siz
                    h+=siz
                lp = l  
        else:
            colorR = (255, 0, 255)
        
        #if detector.fingersUp(hand) == [0,0,0,0,0]:
        #    break
    cv2.rectangle(img, (cx-w//2,cy-h//2), (cx+w//2,cy+h//2), colorR, cv2.FILLED)
    cv2.imshow("img", img)
    cv2.waitKey(1)