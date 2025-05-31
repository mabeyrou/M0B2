from transformers import DetrImageProcessor, DetrForObjectDetection

class DetectionService:
    def __init__(self, threshold=0.9):
        self.processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", 
                                                            revision="no_timm")
        self.model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", 
                                                            revision="no_timm")
        self.threshold = threshold

    def detect_objects(self, frame, target_sizes):
        inputs = self.processor(images=frame, return_tensors="pt")
        outputs = self.model(**inputs)
        results = self.processor.post_process_object_detection(outputs, 
                                                               target_sizes=target_sizes, 
                                                               threshold=self.threshold)[0]
        return self.format_results(results)

    def format_results(self, results):
        return list(map(
            lambda result: {
                "box": [round(i) for i in result[2].tolist()],
                "label": self.get_label_name(result[1].item()),
                "score": round(result[0].item(), 3)
            },
            zip(results["scores"], results["labels"], results["boxes"])
        ))

    def get_label_name(self, label_id: int) -> str:
        return self.model.config.id2label[label_id]
