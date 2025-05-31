from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from webcam_manager import WebcamManager, WebcamNotAvailableError, WebcamFrameError, WebcamStreamError
from loguru import logger

router = APIRouter(prefix='/api/webcam')

manager = WebcamManager()

@router.get('/')
async def root():
    return {'message': 'The webcam object recognition server is up and running'}

@router.get('/start')
async def start_cam():
    try:
        if not manager.start_cam():
            logger.error('Failed starting webcam.')
            raise HTTPException(status_code=500, detail='Failed starting webcam.')
        
        logger.info('Webcam started successfully!')
        return {'message': 'Webcam started successfully!'}
    
    except WebcamNotAvailableError as error:
        raise HTTPException(status_code=500, detail=str(error))
    
    except Exception as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error))

@router.get('/stop')
async def stop_cam():
    if not manager.stop_cam():
        error = 'Failed stoping webcam.'
        logger.error(error)
        raise HTTPException(status_code=500, detail=error)
    
    return {'message': 'Webcam stoped successfully!'}

@router.get('/stream')
async def video_stream():
    try:
        return StreamingResponse(manager.generate_frames(), 
                             media_type="multipart/x-mixed-replace; boundary=frame")
    
    except WebcamFrameError or WebcamStreamError as error:
        raise HTTPException(status_code=400, detail=str(error))
    
    except Exception as error:
        logger.error(str(error))
        raise HTTPException(status_code=500, detail=str(error))
    
@router.get('/status')
async def get_cam_status():
    return {'is_active': manager.get_status()}