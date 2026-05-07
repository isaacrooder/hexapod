import pigpio
import time

# Connect to pigpio daemon
pi = pigpio.pi()

if not pi.connected:
    print("Could not connect to pigpio")
    exit()

# GPIO pin connected to servo signal wire
SERVO_PIN = 18


def move_servo(angle):
    """
    Move servo to specified angle (0-180)
    """

    # Keep angle within limits
    angle = max(0, min(180, angle))

    # Convert angle to pulse width
    pulse_width = 500 + (angle / 180.0) * 2000

    # Send signal to servo
    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)


try:
    while True:
        # Move to 0°
        print("0 degrees")
        move_servo(0)
        time.sleep(1)

        # Move to 90°
        print("90 degrees")
        move_servo(90)
        time.sleep(1)

        # Move to 180°
        print("180 degrees")
        move_servo(180)
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    # Turn off servo pulses
    pi.set_servo_pulsewidth(SERVO_PIN, 0)

    # Disconnect from pigpio
    pi.stop()
