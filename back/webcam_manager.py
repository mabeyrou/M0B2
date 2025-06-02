import threading
import cv2 as cv
import torch
from detection_service import DetectionService
from description_service import DescriptionService
from loguru import logger
from PIL import Image

class WebcamError(Exception):
    """Base class for webcam related exceptions."""
    pass

class WebcamNotAvailableError(WebcamError):
    """Raised when the webcam cannot be accessed."""
    pass

class WebcamFrameError(WebcamError):
    """Raised when the number of frames captured by the webcam is not the expected one."""
    pass

class WebcamStreamError(WebcamError):
    """Raised when an error occurs during webcam streaming."""
    pass

class WebcamManager:
    def __init__(self, detection_interval: int = 3) -> None:
        self.cap = None
        self.is_active = False
        self.lock = threading.Lock()
        self.detection_service = DetectionService()
        self.detection_interval = detection_interval
        self.description_service = DescriptionService()
        self.frame_count = 0
        self.last_results = None
        self.current_frame = None

    def __enter__(self):
        self.start_cam()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_cam()
    
    def start_cam(self) -> bool:
        with self.lock:
            if self.cap is not None:
                self.cap.release()

            self.cap = cv.VideoCapture(0)
            self.cap.set(cv.CAP_PROP_FPS,5) 

            if not self.cap.isOpened():
                error = 'Unable to access the camera.'
                logger.error(error)
                raise WebcamNotAvailableError(error)
            
            self.is_active = True
            self.frame_count = 0
            self.last_results = None

            return True
        
    def stop_cam(self) -> bool:
        with self.lock:
            if self.cap is not None:
                self.cap.release()
                self.cap = None
            
            self.is_active = False
            
            return True
        
    def get_frame(self):
        if not self.is_active or self.cap is None:
            error = 'The camera seems inactive. Exiting ...'
            logger.error(error)
            raise WebcamNotAvailableError(error)
        
        with self.lock:
            success, frame = self.cap.read()
            self.current_frame = frame

            if not success:
                error = "Can't receive frame (stream end?). Exiting ..."
                logger.error(error)
                raise WebcamError(error)

            self.frame_count += 1
        
            gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)   

            width  = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
            height = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)
            target_sizes = torch.tensor([(height, width)])

            if self.frame_count % self.detection_interval == 0 or self.last_results is None:
                self.last_results = self.detection_service.detect_objects(frame, target_sizes)

            if self.last_results:
                for result in self.last_results:
                    box = result['box']
                    label = result['label']
                    score = result['score']
                    cv.rectangle(gray_frame, (box[0], box[1]), 
                                 (box[2], box[3]), 
                                 color=(255,0,0), thickness=2)
                    text = f'{label} ({score})'
                    cv.putText(gray_frame, text, (box[0], box[1] - 10), 
                               fontFace=cv.FONT_HERSHEY_SIMPLEX, 
                               fontScale=0.5, color=(255,0,0), thickness=1)

            ret, buffer = cv.imencode('.jpg', gray_frame, [cv.IMWRITE_JPEG_QUALITY, 70])
            if ret:
                return buffer.tobytes()
            
        return None
    
    def get_snapshot(self):
        image = Image.fromarray(self.current_frame)  
        result = self.description_service.describe(image)
        logger.debug(result)
        return result
    
    def generate_frames(self):
        try:
            while self.is_active:
                frame = self.get_frame()
                if frame is not None:
                    yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                else:
                    error = 'No frame.'
                    logger.error(error)
                    raise WebcamFrameError(error)
        except Exception as error:
            logger.error(str(error))
            raise WebcamStreamError(str(error))
        
    def get_status(self) -> bool:
        return self.is_active