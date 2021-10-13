import os
import logging
import threading
import time
import subprocess
from rtsparty import Stream
from objectdaddy import Daddy
from relay_controller import RelayController


class ZombieArm():

    def __init__(self):
        logging.info('Starting Zombie Arm')
        self.person_detected = False
        self.last_detected = self._get_time()
        self.arm_activity_timeout = 5
        self.arm_extend_timeout = 2
        self.arm_hold_timeout = 2
        self.arm_retract_timeout = 3
        self._setup_stream()
        self._setup_object_recognition()
        self._setup_relay()
    
    def _get_time(self):
        """Return the current time in unix seconds"""
        return int(time.time())

    def _setup_stream(self):
        """Set up the stream to the camera"""
        logging.info('Starting stream')
        self.stream = Stream(os.environ.get('STREAM_URL'))

    def _setup_object_recognition(self):
        """Set up object recognition and load models"""
        logging.info('Loading ML models')
        self.daddy = Daddy()
        self.daddy.set_callbacks(self.object_detected, self.object_expired)

    def _setup_relay(self):
        """Set up the relay controller"""
        self.rc = RelayController()

    def object_detected(self, detection):
        """Callback for an object being detected"""
        logging.info(f'{detection.label} detected')
        try:
            if detection.is_person():
                self.activate_arm()
        except Exception:
            pass

    def _should_arm_activate(self):
        """Checks if the arm should activate"""
        current = self._get_time()
        timed_out_at = self.last_detected + self.arm_activity_timeout
        return current > timed_out_at
    
    def _cycle_arm(self):
        """Cycle the arm"""
        self.rc.extend_arm(self.arm_extend_timeout)
        time.sleep(self.arm_hold_timeout)
        self.rc.retract_arm(self.arm_retract_timeout)

    def activate_arm(self):
        """Activate the zombie arm"""
        if not self._should_arm_activate():
            logging.info('Not activating arm; within timeout')
            return
        self._cycle_arm()

    def object_expired(self, detection):
        """Callback for an object expiring"""
        logging.info(f'{detection.label} expired')
        try:
            if detection.is_person():
                self.last_detected = self.get_time()
        except Exception:
            pass

    def process_frames_from_stream(self):
        """Processes the frames from the stream"""
        while True:
            logging.debug('Checking Frame')
            frame = self.stream.get_frame()
            if self.stream.is_frame_empty(frame):
                continue
            self.latest_frame = frame
            self.daddy.process_frame(frame)

    def run(self):
        """Run the application"""
        logging.info('Testing Arm:')
        self._cycle_arm()
        try:
            self.process_frames_from_stream()
        except KeyboardInterrupt:
            logging.info('Exiting application')


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    za = ZombieArm()
    za.run()
