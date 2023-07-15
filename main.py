import cv2



def faceBox(fNet,frame):
    frameH=frame.shape[0]
    frameW=frame.shape[1]
    blob=cv2.dnn.blobFromImage(frame,1.0,(227,227),[104,117,123],swapRB=False)
    fNet.setInput(blob)
    detection=fNet.forward()
    bboxs=[]
    
    for i in range(detection.shape[2]):
        confidence=detection[0,0,i,2]
        if confidence>0.7:
            x1=int(detection[0,0,i,3]*frameW)
            y1=int(detection[0,0,i,4]*frameH)
            x2=int(detection[0,0,i,5]*frameW)
            y2=int(detection[0,0,i,6]*frameH)
            bboxs.append([x1,y1,x2,y2])
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),1)
    return frame,bboxs

fProto="opencv_face_detector.pbtxt"
fModel="opencv_face_detector_uint8.pb"


age="images.prototxt"
people="worldpeople.caffemodel"

MODEL_MEAN_VALUES=(78.4263377603,87.7689143744,114.895847746)
fNet=cv2.dnn.readNet(fModel,fProto)
aNet=cv2.dnn.readNet(age,people)

ageList= ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(21-36)', '(38-43)', '(48-53)', '(60-100)']

video=cv2.VideoCapture(0)
padding=20
while True:
    ret,frame=video.read()
    frame,bboxs=faceBox(fNet,frame)
    for bbox in bboxs:
        #face=frame[bbox[1]:bbox[3],bbox[0]:bbox[2]]
        face=frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding,frame.shape[1]-1)]
        blob=cv2.dnn.blobFromImage(face,1.0,(227,227),MODEL_MEAN_VALUES,swapRB=False)
        aNet.setInput(blob)
        agePred=aNet.forward()
        age=ageList[agePred[0].argmax()]



        label="{}".format(age)
        cv2.rectangle(frame,(bbox[0],bbox[1]-30),(bbox[2],bbox[1]),(0,255,0),-1)
        cv2.putText(frame,label,(bbox[0],bbox[1]-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow("Age",frame)
    k=cv2.waitKey(1)
    if k==ord('q'):
        break
video.release()
cv2.destroyAllWindows()
