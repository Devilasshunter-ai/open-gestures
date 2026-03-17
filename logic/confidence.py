class Confidence:
    def __init__(self, threshold=3):
        self.threshold = threshold
        self.current_gesture = None
        self.frame_count = 0

    def update(self, gesture):
        if gesture == self.current_gesture:
            self.frame_count += 1
        else:
            self.current_gesture = gesture
            self.frame_count = 1

    def reset(self):
        self.current_gesture = None
        self.frame_count = 0

    def confirmed(self):
        return self.frame_count >= self.threshold
        self.reset()
