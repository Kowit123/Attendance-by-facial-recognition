import time

class AttendanceGuard:
    def __init__(self, cooldown_seconds=300):
        self.cooldown = cooldown_seconds
        self.last_seen = {}

    def can_mark(self, student_id):
        now = time.time()

        if student_id not in self.last_seen:
            return True

        return (now - self.last_seen[student_id]) >= self.cooldown

    def mark(self, student_id):
        self.last_seen[student_id] = time.time()

