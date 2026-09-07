import os
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class ObjectDetector:
    """
    Computer Vision Object & Behavioral Action Detector.
    Uses Google MediaPipe EfficientDet-Lite0 for 'cell phone', 'bottle', 'cup' object detection,
    plus Hand Landmarker for Hand-to-Ear / Calling posture analysis.
    Provides fast, robust real-time phone tracking.
    """
    def __init__(self, temporal_threshold_frames=3):
        self.temporal_threshold = temporal_threshold_frames
        self.phone_frames = 0
        self.drinking_frames = 0
        self.seatbelt_frames = 0

        self.supported_classes = ["person", "cell phone", "bottle", "cup"]

        # Models Path
        base_dir = os.path.dirname(os.path.abspath(__file__))
        obj_model_path = os.path.join(base_dir, "models", "efficientdet_lite0.tflite")
        hand_model_path = os.path.join(base_dir, "models", "hand_landmarker.task")

        self.obj_detector = None
        self.hand_detector = None

        # Initialize Object Detector
        if os.path.exists(obj_model_path):
            try:
                base_options = python.BaseOptions(model_asset_path=obj_model_path)
                options = vision.ObjectDetectorOptions(
                    base_options=base_options, 
                    score_threshold=0.25,
                    max_results=5
                )
                self.obj_detector = vision.ObjectDetector.create_from_options(options)
            except Exception as e:
                print(f"[ObjectDetector] Warning: Could not init EfficientDet: {e}")

        # Initialize Hand Detector
        if os.path.exists(hand_model_path):
            try:
                hand_options = python.BaseOptions(model_asset_path=hand_model_path)
                hand_det_opts = vision.HandLandmarkerOptions(
                    base_options=hand_options, 
                    num_hands=2,
                    min_hand_detection_confidence=0.3,
                    min_hand_presence_confidence=0.3
                )
                self.hand_detector = vision.HandLandmarker.create_from_options(hand_det_opts)
            except Exception as e:
                print(f"[ObjectDetector] Warning: Could not init HandLandmarker: {e}")

    def detect_seatbelt(self, frame, face_bbox):
        """
        Analyzes lower chest/shoulder ROI for diagonal strap line contrast features.
        """
        if face_bbox is None:
            return "UNKNOWN / LOW CONFIDENCE", 0.0

        fx, fy, fw, fh = face_bbox
        h, w, _ = frame.shape

        roi_top = min(h - 10, fy + fh)
        roi_bottom = min(h, fy + int(fh * 2.8))
        roi_left = max(0, fx - int(fw * 0.5))
        roi_right = min(w, fx + int(fw * 1.5))

        chest_roi = frame[roi_top:roi_bottom, roi_left:roi_right]
        if chest_roi.size == 0 or chest_roi.shape[0] < 20 or chest_roi.shape[1] < 20:
            return "UNKNOWN / LOW CONFIDENCE", 0.20

        gray = cv2.cvtColor(chest_roi, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=45, minLineLength=35, maxLineGap=10)
        
        diagonal_line_found = False
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angle = abs(np.degrees(np.arctan2(y2 - y1, x2 - x1)))
                if 25.0 <= angle <= 65.0:
                    diagonal_line_found = True
                    break

        if diagonal_line_found:
            self.seatbelt_frames = min(20, self.seatbelt_frames + 1)
        else:
            self.seatbelt_frames = max(0, self.seatbelt_frames - 1)

        if self.seatbelt_frames >= self.temporal_threshold:
            return "SEATBELT DETECTED", 0.85
        elif self.seatbelt_frames > 0:
            return "UNKNOWN / LOW CONFIDENCE", 0.45
        else:
            return "SEATBELT NOT DETECTED", 0.20

    def update(self, frame, face_detection=None):
        """
        Runs object detection and hand position analysis to detect phone usage, drinking, and seatbelt.
        """
        h, w, _ = frame.shape
        mp_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=mp_rgb)

        raw_phone_found = False
        raw_drinking_found = False
        phone_boxes = []
        phone_reason = ""
        phone_conf = 0.0

        # 1. Google MediaPipe EfficientDet Object Detection
        if self.obj_detector:
            try:
                detection_result = self.obj_detector.detect(mp_image)
                for det in detection_result.detections:
                    for category in det.categories:
                        cat_name = category.category_name.lower()
                        score = category.score
                        bbox = det.bounding_box
                        
                        bx = int(bbox.origin_x)
                        by = int(bbox.origin_y)
                        bw = int(bbox.width)
                        bh = int(bbox.height)

                        if cat_name in ["cell phone", "mobile phone", "phone"] and score > 0.20:
                            raw_phone_found = True
                            phone_conf = max(phone_conf, float(score))
                            phone_boxes.append({
                                "bbox": (bx, by, bw, bh),
                                "label": f"PHONE: {int(score * 100)}%",
                                "confidence": score
                            })
                            phone_reason = "PHONE IN HAND / FRAME"

                        elif cat_name in ["bottle", "cup"] and score > 0.30:
                            raw_drinking_found = True
            except Exception as e:
                pass

        # 2. Hand Position & Ear Proximity Analysis (Hand-to-Ear Calling Posture)
        if face_detection and "bbox" in face_detection:
            fx, fy, fw, fh = face_detection["bbox"]
            face_center_x = fx + fw / 2.0
            face_center_y = fy + fh / 2.0

            # Left and right ear regions in pixel space
            left_ear_x, left_ear_y = max(0, fx - int(fw * 0.25)), fy + int(fh * 0.45)
            right_ear_x, right_ear_y = min(w, fx + int(fw * 1.25)), fy + int(fh * 0.45)

            if self.hand_detector:
                try:
                    hand_result = self.hand_detector.detect(mp_image)
                    if hand_result.hand_landmarks:
                        for hand_lms in hand_result.hand_landmarks:
                            # Wrist (0) and Index Tip (8) landmarks
                            wrist_x = int(hand_lms[0].x * w)
                            wrist_y = int(hand_lms[0].y * h)
                            index_x = int(hand_lms[8].x * w)
                            index_y = int(hand_lms[8].y * h)

                            # Check distance to left or right ear
                            dist_left_ear = np.hypot(index_x - left_ear_x, index_y - left_ear_y)
                            dist_right_ear = np.hypot(index_x - right_ear_x, index_y - right_ear_y)
                            
                            ear_threshold = fw * 0.9  # normalized to face width

                            if dist_left_ear < ear_threshold or dist_right_ear < ear_threshold:
                                raw_phone_found = True
                                phone_conf = max(phone_conf, 0.88)
                                phone_reason = "PHONE CALL (HAND TO EAR)"
                                
                                hx = min(wrist_x, index_x) - 20
                                hy = min(wrist_y, index_y) - 20
                                hw_box = abs(wrist_x - index_x) + 40
                                hh_box = abs(wrist_y - index_y) + 40
                                phone_boxes.append({
                                    "bbox": (max(0, hx), max(0, hy), hw_box, hh_box),
                                    "label": "CALLING: HAND TO EAR",
                                    "confidence": 0.88
                                })
                except Exception as e:
                    pass

        # 3. Temporal Debouncing for Phone
        if raw_phone_found:
            self.phone_frames = min(20, self.phone_frames + 1)
        else:
            self.phone_frames = max(0, self.phone_frames - 1)

        is_phone_active = self.phone_frames >= self.temporal_threshold

        if is_phone_active:
            phone_status = f"PHONE: DETECTED ({phone_reason or 'ACTIVE'})"
            if phone_conf == 0.0:
                phone_conf = 0.80
        else:
            phone_status = "PHONE: NOT IN USE"
            phone_conf = 0.0
            phone_boxes = []

        # 4. Temporal Debouncing for Drinking
        if raw_drinking_found:
            self.drinking_frames = min(20, self.drinking_frames + 1)
        else:
            self.drinking_frames = max(0, self.drinking_frames - 1)

        is_drinking_active = self.drinking_frames >= self.temporal_threshold
        drinking_status = "DRINKING: DETECTED" if is_drinking_active else "DRINKING: NOT DETECTED"

        # 5. Seatbelt Detection
        seatbelt_status, seatbelt_confidence = "UNKNOWN / LOW CONFIDENCE", 0.30
        if face_detection and "bbox" in face_detection:
            seatbelt_status, seatbelt_confidence = self.detect_seatbelt(frame, face_detection["bbox"])

        return {
            "possible_phone_detected": is_phone_active,
            "phone_status": phone_status,
            "phone_confidence": phone_conf,
            "phone_reason": phone_reason,
            "phone_boxes": phone_boxes,
            "possible_drinking_detected": is_drinking_active,
            "drinking_status": drinking_status,
            "drinking_confidence": 0.80 if is_drinking_active else 0.0,
            "smoking_status": "SMOKING: UNKNOWN / NOT SUPPORTED BY MODEL",
            "smoking_confidence": 0.0,
            "seatbelt_status": seatbelt_status,
            "seatbelt_confidence": seatbelt_confidence,
            "supported_classes": self.supported_classes
        }
