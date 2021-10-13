import logging
import time
import RPi.GPIO as GPIO


class RelayController():
    """Class for controlling the relay"""

    def __init__(self):
        self._set_defaults()
        self._setup_gpio()

    def __del__(self):
        GPIO.cleanup()

    def _set_defaults(self):
        """Set defaults for the application"""
        self.silent = False
        self.arm_extend_pin = 8
        self.arm_retract_pin = 10

    def _setup_gpio(self):
        """Set up the GPIO defaults"""
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.arm_extend_pin, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.arm_retract_pin, GPIO.OUT, initial=GPIO.HIGH)

    def extend_arm(self, timeout):
        """Extends the arm and waits"""
        logging.info('Extending Arm')
        self._cycle_pin(self.arm_extend_pin, timeout)

    def retract_arm(self, timeout):
        """Retracts the arm and waits"""
        logging.info('Retracting Arm')
        self._cycle_pin(self.arm_extend_pin, timeout)

    def _cycle_pin(self, pin, timeout):
        """Cycle a relay channel on and off"""
        GPIO.output(pin, 0)
        time.sleep(timeout)
        GPIO.output(pin, 1)
