import threading
import cv2 as cv

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
    def __init__(self) -> None:
        self.cap = None
        self.is_active = False
        self.lock = threading.Lock()
    
    def start_cam(self) -> bool:
        with self.lock:
            if self.cap is not None:
                self.cap.release()

            self.cap = cv.VideoCapture(0)

            if not self.cap.isOpened():
                raise WebcamNotAvailableError('Unable to access the camera.')
            
            self.is_active = True
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
            raise WebcamNotAvailableError('The camera seems inactive. Exiting ...')
        
        with self.lock:
            success, frame = self.cap.read()

            if not success:
                raise WebcamError("Can't receive frame (stream end?). Exiting ...")
        
            ret, buffer = cv.imencode('.jpg', frame, [cv.IMWRITE_JPEG_QUALITY, 85])
            if ret:
                return buffer.tobytes()
            
        return None
    
    def generate_frames(self):
        try:
            while self.is_active:
                frame = self.get_frame()
                if frame is not None:
                    # yield frame
                    yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                else:
                    raise WebcamFrameError('No frame.')
        except Exception as error:
            raise WebcamStreamError(str(error))