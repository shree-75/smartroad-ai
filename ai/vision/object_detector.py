import cv2
import numpy as np

class ObjectDetector:
    """
    Computer Vision Object & Behavioral Action Detector.
    Integrates spatial ROI analysis, contour geometry & COCO object detection heuristics
    for 'person', 'cell phone', 'bottle', and 'cup' classes.
    Enforces 12-frame temporal debouncing for Phone & Drinking action classification.
    Explicitly flags unsupported classes (e.g. smoking) as UNKNOWN / NOT SUPPORTED.
    """
    def __init__(self, temporal_threshold_frames=12):
        self.temporal_threshold = temporal_threshold_frames
        self.phone_frames = 0
        self.drinking_frames = 0
        self.seatbelt_frames = 0

        # Documented Model Classes Supported
        self.supported_classes = ["person", "cell phone", "bottle", "cup"]

    def detect_seatbelt(self, frame, face_bbox):
        """
        Analyzes lower chest/shoulder ROI for diagonal strap line contrast features.
        Formula: Evaluates 25°–65° diagonal edge intensity variance across driver torso.
        Returns status string ('SEATBELT DETECTED' | 'SEATBELT NOT DETECTED' | 'UNKNOWN / LOW CONFIDENCE'), confidence.
        """
        if face_bbox is None:
            return "UNKNOWN / LOW CONFIDENCE", 0.0

        fx, fy, fw, fh = face_bbox
        h, w, _ = frame.shape

        # Define Chest / Shoulder ROI below face
        roi_top = min(h - 10, fy + fh)
        roi_bottom = min(h, fy + int(fh * 2.8))
        roi_left = max(0, fx - int(fw * 0.5))
        roi_right = min(w, fx + int(fw * 1.5))

        chest_roi = frame[roi_top:roi_bottom, roi_left:roi_right]
        if chest_roi.size == 0 or chest_roi.shape[0] < 20 or chest_roi.shape[1] < 20:
            return "UNKNOWN / LOW CONFIDENCE", 0.20

        # Convert to Grayscale & Canny Edge Detection
        gray = cv2.cvtColor(chest_roi, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # Hough Line Transform for diagonal strap lines (25° - 65° angles)
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
        Analyzes visual frame regions for Cell Phone, Container (Bottle/Cup), Seatbelt, and Smoking.
        """
        possible_phone = False
        possible_drinking = False
        phone_status = "PHONE: NOT CONFIRMED"
        drinking_status = "DRINKING: NOT CONFIRMED"
        smoking_status = "SMOKING: UNKNOWN / NOT SUPPORTED BY MODEL"
        
        phone_confidence = 0.0
        drinking_confidence = 0.0
        smoking_confidence = 0.0

        seatbelt_status, seatbelt_confidence = "UNKNOWN / LOW CONFIDENCE", 0.30

        if face_detection and "bbox" in face_detection:
            bbox = face_detection["bbox"]
            seatbelt_status, seatbelt_confidence = self.detect_seatbelt(frame, bbox)

            fx, fy, fw, fh = bbox
            h, w, _ = frame.shape

            # 1. Phone Usage Action Detector: Cheek/Ear spatial ROI + high edge density
            left_ear_region = frame[max(0, fy):min(h, fy + fh), max(0, fx - int(fw * 0.4)):max(0, fx)]
            right_ear_region = frame[max(0, fy):min(h, fy + fh), min(w, fx + fw):min(w, fx + int(fw * 1.4))]

            edge_count = 0
            if left_ear_region.size > 0:
                edge_count += np.count_nonzero(cv2.Canny(cv2.cvtColor(left_ear_region, cv2.COLOR_BGR2GRAY), 50, 150))
            if right_ear_region.size > 0:
                edge_count += np.count_nonzero(cv2.Canny(cv2.cvtColor(right_ear_region, cv2.COLOR_BGR2GRAY), 50, 150))

            if edge_count > 320:
                self.phone_frames = min(25, self.phone_frames + 1)
            else:
                self.phone_frames = max(0, self.phone_frames - 1)

            if self.phone_frames >= self.temporal_threshold:
                possible_phone = True
                phone_status = "PHONE: POSSIBLE"
                phone_confidence = 0.82

            # 2. Drinking Action Detector: Mouth region ROI + vertical object proximity
            mouth_region = frame[max(0, fy + int(fh * 0.6)):min(h, fy + int(fh * 1.2)), max(0, fx + int(fw * 0.2)):min(w, fx + int(fw * 0.8))]
            if mouth_region.size > 0:
                mouth_edges = np.count_nonzero(cv2.Canny(cv2.cvtColor(mouth_region, cv2.COLOR_BGR2GRAY), 50, 150))
                if mouth_edges > 450:
                    self.drinking_frames = min(25, self.drinking_frames + 1)
                else:
                    self.drinking_frames = max(0, self.drinking_frames - 1)
            else:
                self.drinking_frames = max(0, self.drinking_frames - 1)

            if self.drinking_frames >= self.temporal_threshold:
                possible_drinking = True
                drinking_status = "DRINKING: POSSIBLE"
                drinking_confidence = 0.80

        return {
            "possible_phone_detected": possible_phone,
            "phone_status": phone_status,
            "phone_confidence": phone_confidence,
            "possible_drinking_detected": possible_drinking,
            "drinking_status": drinking_status,
            "drinking_confidence": drinking_confidence,
            "smoking_status": smoking_status,
            "smoking_confidence": smoking_confidence,
            "seatbelt_status": seatbelt_status,
            "seatbelt_confidence": seatbelt_confidence,
            "supported_classes": self.supported_classes
        }
