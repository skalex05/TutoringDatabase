from threading import Thread
from sched import scheduler
import time

class EventScheduler(Thread):
    exists = False
    def __init__(self, check_session_for_schedule):
        self.check_session_for_schedule = check_session_for_schedule
        self.scheduler = scheduler(time.time, time.sleep)
        self.scheduled_sessions = {}
        super().__init__()

    def run(self):
        if EventScheduler.exists:
            return
        EventScheduler.exists = True
        while self.is_alive():
            self.scheduler.run(blocking=False)
            time.sleep(1)

    def schedule_session(self, session_id, time=0):
        self.remove_session(session_id)
        self.scheduled_sessions[session_id] = self.scheduler.enterabs(time, 0,
                                                                      action=self.check_session_for_schedule,

                                                                      argument=(session_id,))

    def remove_session(self, session_id):
        if session_id in self.scheduled_sessions:
            try:
                self.scheduler.cancel(self.scheduled_sessions[session_id])
            except ValueError:
                pass
            del self.scheduled_sessions[session_id]

