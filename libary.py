# hexapod.py
#
# Simple hexapod walking library using pigpio
# Assumes:
# - 6 legs
# - each leg has 2 servos:
#     hip  = forward/back movement
#     knee = up/down movement
#
# You can expand this later for 3DOF legs.

import pigpio
import time


class Servo:
    def __init__(self, pi, pin, min_pw=600, max_pw=2300):
        self.pi = pi
        self.pin = pin
        self.min_pw = min_pw
        self.max_pw = max_pw

    def move(self, angle):
        angle = max(0, min(180, angle))

        pulse = self.min_pw + (angle / 180.0) * (
            self.max_pw - self.min_pw
        )

        self.pi.set_servo_pulsewidth(self.pin, pulse)


class Leg:
    def __init__(self, hip, knee):
        self.hip = hip
        self.knee = knee

    def liftleft(self):
        self.knee.move(150)

    def lowerleft(self):
        self.knee.move(0)

    def forwardleft(self):
        self.hip.move(60)

    def backwardleft(self):
        self.hip.move(60)
        
    def liftright(self):
        self.knee.move(30)

    def lowerright(self):
        self.knee.move(175)

    def forwardright(self):
        self.hip.move(120)
        

    def backwardright(self):
        self.hip.move(120)

    def centerleft(self):
        self.hip.move(120)
    
    def centerright(self):
        self.hip.move(60)


class Hexapod:
    def __init__(self):
        self.pi = pigpio.pi()

        if not self.pi.connected:
            raise RuntimeError("Could not connect to pigpio")

        # ===== CHANGE THESE GPIO PINS =====
        self.legs = [
            Leg(Servo(self.pi, 2),  Servo(self.pi, 3)),   # Front Left
            Leg(Servo(self.pi, 4),  Servo(self.pi, 17)),  # Middle Left
            Leg(Servo(self.pi, 27), Servo(self.pi, 22)),  # Rear Left

            Leg(Servo(self.pi, 10), Servo(self.pi, 9)),   # Front Right
            Leg(Servo(self.pi, 11), Servo(self.pi, 5)),   # Middle Right
            Leg(Servo(self.pi, 6),  Servo(self.pi, 13)),  # Rear Right
        ]

        # Tripod gait groups
        self.group_a = [
            self.legs[0],  # Front Left
            self.legs[2],  # Rear Left
            self.legs[4],  # Middle Right
        ]

        self.group_b = [
            self.legs[1],  # Middle Left
            self.legs[3],  # Front Right
            self.legs[5],  # Rear Right
        ]

    def stand(self):
        for leg in self.legs:
            leg.center()
            leg.lower()

    def move_group_forward(self, group):
        for leg in group:
            leg.lift()

        time.sleep(0.1)

        for leg in group:
            leg.forward()

        time.sleep(0.1)

        for leg in group:
            leg.lower()

        time.sleep(0.1)

    def move_group_backward(self, group):
        for leg in group:
            leg.backward()

        time.sleep(0.1)

    def walk_forward(self, steps=1):

        for _ in range(steps):

            # Move tripod A
            self.move_group_forward(self.group_a)
            self.move_group_backward(self.group_b)

            # Move tripod B
            self.move_group_forward(self.group_b)
            self.move_group_backward(self.group_a)

    def stop(self):
        for leg in self.legs:
            leg.hip.pi.set_servo_pulsewidth(leg.hip.pin, 0)
            leg.knee.pi.set_servo_pulsewidth(leg.knee.pin, 0)

        self.pi.stop()
