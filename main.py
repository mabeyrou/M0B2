import cv2 as cv
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from loguru import logger
from fastapi import FastAPI

app = FastAPI()

@app.get("/video_stream")
async def get_video_stream():
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
    
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        ret, frame = cap.read()
    
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        inputs = processor(images=frame, return_tensors="pt")
        outputs = model(**inputs)

        width  = cap.get(cv.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv.CAP_PROP_FRAME_HEIGHT) 

        target_sizes = torch.tensor([(width, height)[::-1]])
        results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i) for i in box.tolist()]
            cv.rectangle(gray_frame, (box[0], box[1]), (box[2], box[3]), color=(255,0,0), thickness=2)
            cv.putText(gray_frame, model.config.id2label[label.item()], (box[0], box[1] - 10), fontFace=cv.FONT_HERSHEY_SIMPLEX, 
                    fontScale=0.5, color=(255,0,0), thickness=1)

        bgr_frame = cv.cvtColor(gray_frame, cv.COLOR_GRAY2BGR)
        cv.imshow('frame', bgr_frame)
        
        if cv.waitKey(1) == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()