import cv2
import numpy as np
import mediapipe as mp
import math
import time
import random

# --- Helper Class for State Management & Cooldown ---
class StateManager:
    def __init__(self, cooldown=1.0):
        self.last_gesture_time = 0
        self.cooldown = cooldown

    def check_cooldown(self):
        return time.time() - self.last_gesture_time > self.cooldown

    def reset_cooldown(self):
        self.last_gesture_time = time.time()

# --- Main Application Class ---
class HandDrawingApp:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.8, max_num_hands=2, min_tracking_confidence=0.5)

        self.gesture_manager = StateManager(cooldown=0.5)
        self.background_colors = [(10, 10, 10), (10, 10, 50), (10, 50, 10), (50, 10, 10)]
        self.background_index = 0
        self.canvas = np.full((720, 1280, 3), self.background_colors[self.background_index], dtype="uint8")

        self.VIBRANT_YELLOW = (0, 255, 255)
        self.VIBRANT_PINK = (255, 0, 255)
        self.VIBRANT_CYAN = (255, 255, 0)

        self.draw_color = self.VIBRANT_YELLOW
        self.brush_thickness = 15
        self.active_button = "yellow"
        self.prev_points = {0: None, 1: None}
        self.is_drawing = False
        self.special_brush = None
        self.particles = []

        self.ui_buttons = {
            "red": [(10, 10, 110, 60), (0, 0, 200)],
            "green": [(130, 10, 230, 60), (0, 200, 0)],
            "blue": [(250, 10, 350, 60), (200, 100, 0)],
            "yellow": [(370, 10, 470, 60), self.VIBRANT_YELLOW],
            "pink": [(490, 10, 590, 60), self.VIBRANT_PINK],
            "cyan": [(610, 10, 710, 60), self.VIBRANT_CYAN],
            "eraser": [(1060, 10, 1160, 60), (40, 40, 40), "ERASE"],
            "exit": [(1180, 10, 1270, 60), (0, 0, 100), "EXIT"],
        }

        print("\n--- Hand Drawing App Initialized ---")
        print("Right Hand: Drawing/Clicking | Left Hand: Brush Size/Gestures")

    def _is_finger_up(self, hand_landmarks, tip_index, pip_index):
        return hand_landmarks.landmark[tip_index].y < hand_landmarks.landmark[pip_index].y

    def _count_fingers(self, hand_landmarks):
        finger_tips = [8, 12, 16, 20]
        thumb_tip = 4
        count = 0
        for tip in finger_tips:
            if self._is_finger_up(hand_landmarks, tip, tip - 2):
                count += 1
        if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
            count += 1
        return count

    def _handle_left_hand(self, hand_landmarks, frame_w, frame_h):
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        ix, iy = int(index_tip.x * frame_w), int(index_tip.y * frame_h)
        tx, ty = int(thumb_tip.x * frame_w), int(thumb_tip.y * frame_h)

        size_dist = math.hypot(tx - ix, ty - iy)
        self.brush_thickness = int(np.interp(size_dist, [30, 200], [5, 100]))

        cv2.line(self.frame, (tx, ty), (ix, iy), (255, 255, 0), 3)
        cv2.circle(self.frame, (ix, iy), self.brush_thickness // 2, (255, 255, 0), -1)

        if self.gesture_manager.check_cooldown():
            fingers_up = self._count_fingers(hand_landmarks)
            if fingers_up == 5:
                print("TERMINAL: Left Hand Gesture - Open Palm (Particle Animation)")
                for _ in range(30):
                    start_pos = [random.randint(0, frame_w), 0]
                    velocity = [random.uniform(-1, 1), random.uniform(2, 5)]
                    self.particles.append([start_pos, velocity, random.randint(5, 12), (255, 255, random.randint(150, 255))])
                self.gesture_manager.reset_cooldown()

            elif fingers_up == 0:
                print("TERMINAL: Left Hand Gesture - Fist (Clear Canvas)")
                self.canvas[:] = self.background_colors[self.background_index]
                self.gesture_manager.reset_cooldown()

            elif fingers_up == 1:
                print("TERMINAL: Left Hand Gesture - 1 Finger (Change Background)")
                self.background_index = (self.background_index + 1) % len(self.background_colors)
                self.canvas[:] = self.background_colors[self.background_index]
                self.gesture_manager.reset_cooldown()

    def _handle_right_hand(self, hand_landmarks, frame_w, frame_h):
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        ix, iy = int(index_tip.x * frame_w), int(index_tip.y * frame_h)
        tx, ty = int(thumb_tip.x * frame_w), int(thumb_tip.y * frame_h)

        # Cursor
        cv2.circle(self.frame, (ix, iy), 8, (255, 255, 255), -1)
        cv2.putText(self.frame, "Cursor", (ix + 10, iy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        click_dist = math.hypot(int(middle_tip.x * frame_w) - ix, int(middle_tip.y * frame_h) - iy)
        draw_dist = math.hypot(tx - ix, ty - iy)

        if draw_dist < 40:
            self.is_drawing = True
        elif draw_dist > 60:
            self.is_drawing = False

        is_over_ui = False
        if click_dist < 40:
            self.is_drawing = False
            for key, val in self.ui_buttons.items():
                x1, y1, x2, y2 = val[0]
                if x1 < ix < x2 and y1 < iy < y2:
                    is_over_ui = True
                    if key == "exit":
                        self.running = False
                    elif key == "eraser":
                        self.active_button = "eraser"
                    else:
                        self.draw_color, self.active_button = val[1], key
                    print(f"TERMINAL: UI Click - Selected '{key.upper()}'")
                    break

        if self.is_drawing and not is_over_ui:
            effective_color = self.background_colors[self.background_index] if self.active_button == "eraser" else self.draw_color
            prev_point = self.prev_points.get(1)
            if prev_point is None:
                prev_point = (ix, iy)
            cv2.line(self.canvas, prev_point, (ix, iy), effective_color, self.brush_thickness)
            self.prev_points[1] = (ix, iy)
        else:
            self.prev_points[1] = None

    def run(self):
        self.running = True
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)

        while self.running and cap.isOpened():
            ret, self.frame = cap.read()
            if not ret:
                break

            self.frame = cv2.flip(self.frame, 1)
            h, w, _ = self.frame.shape

            rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            persistent_canvas = np.copy(self.canvas)
            self.frame = cv2.addWeighted(self.frame, 0.6, persistent_canvas, 0.4, 0)

            for p in self.particles:
                p[0][0] += p[1][0]
                p[0][1] += p[1][1]
                p[2] -= 0.5
                if p[2] > 0:
                    cv2.circle(self.frame, tuple(map(int, p[0])), int(p[2]), p[3], -1)
            self.particles = [p for p in self.particles if p[2] > 0]

            for key, val in self.ui_buttons.items():
                cv2.rectangle(self.frame, val[0][:2], val[0][2:], val[1], -1)
                if len(val) > 2:
                    cv2.putText(self.frame, val[2], (val[0][0] + 15, val[0][1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                if key == self.active_button:
                    cv2.rectangle(self.frame, val[0][:2], val[0][2:], (255, 255, 255), 3)

            finger_counts = "Fingers - L:? R:?"
            if results.multi_hand_landmarks:
                left_fingers, right_fingers = "?", "?"
                for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    handedness = results.multi_handedness[i].classification[0].label
                    if handedness == "Left":
                        left_fingers = self._count_fingers(hand_landmarks)
                        self._handle_left_hand(hand_landmarks, w, h)
                    else:
                        right_fingers = self._count_fingers(hand_landmarks)
                        self._handle_right_hand(hand_landmarks, w, h)
                finger_counts = f"Fingers - L:{left_fingers} R:{right_fingers}"

            cv2.putText(self.frame, finger_counts, (w - 300, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            cv2.putText(self.frame, f"Size: {self.brush_thickness}", (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            cv2.imshow("Hand Tracking Drawing App", self.frame)

            if cv2.waitKey(5) & 0xFF == 27:
                self.running = False

        print("\n--- Exiting Application ---")
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    app = HandDrawingApp()
    app.run()
