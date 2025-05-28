from transformers import DetrImageProcessor, DetrForObjectDetection

class DetectionService:
    def __init__(self):
        self.processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", 
                                                            revision="no_timm")
        self.model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", 
                                                            revision="no_timm")

    def detect_objects(self, frame, target_sizes):
        inputs = self.processor(images=frame, return_tensors="pt")
        outputs = self.model(**inputs)
        results = self.processor.post_process_object_detection(outputs, 
                                                               target_sizes=target_sizes, 
                                                               threshold=0.9)[0]
        return results

    def get_label_name(self, label_id: int) -> str:
        return self.model.config.id2label[label_id]
