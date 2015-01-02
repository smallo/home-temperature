__author__ = 'sergiom'

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Could not import RPi.GPIO!!! Try running as root")
except ImportError:
    print("Could not import RPi.GPIO!!! Ignore if you are using mocks")


class ActivatorMock():
    def __init__(self, pin):
        self.pin = pin
        self.status = False

    def activate(self):
        self.status = True
        print 'Pin {0} activated'.format(self.pin)

    def deactivate(self):
        self.status = False
        print 'Pin {0} deactivated'.format(self.pin)

    def get_status(self):
        print 'Activator status for pin {0}: {1}'.format(self.pin, self.status)
        return self.status

class ActivatorRpiGpio():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM) # Change this to GPIO.BOARD
        GPIO.setup(pin, GPIO.OUT)

    def activate(self):
        GPIO.output(self.pin, True)

    def deactivate(self):
        GPIO.output(self.pin, False)

    def get_status(self):
        return GPIO.input(self.pin)
