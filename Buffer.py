from adafruit_servokit import ServoKit
from time import sleep

kit = ServoKit(channels=16)

# -----------------------------
# SERVO MAP
# -----------------------------

L1K, L1H = 0, 1
L2K, L2H = 2, 3
L3K, L3H = 4, 5
L4K, L4H = 6, 7
L5K, L5H = 8, 9
L6K, L6H = 10, 11

KNEES = [L1K, L2K, L3K, L4K, L5K, L6K]
HIPS  = [L1H, L2H, L3H, L4H, L5H, L6H]
# -----------------------------
# CALIBRATION 
# -----------------------------

HIP_BACK = 120
HIP_FORWARD = 60

KNEE_DOWN = 5
KNEE_UP = 100

CENTER = 90

HIP_STEP = 45


# -----------------------------
# Knee inversion
# -----------------------------

INVERT_KNEES = {2, 6, 10}
INVERT_HIP = {3, 7, 11}  # right-side knees likely flipped

def set_servo(ch, angle):
    kit.servo[ch].angle = max(0, min(180, angle))

def set_knee(ch, angle):
    if ch in INVERT_KNEES:
        angle = 175 - angle
    set_servo(ch, angle)

def set_hip(ch, angle):
    if ch in INVERT_HIP:
        angle = 160 - angle
    set_servo(ch, angle)

# -----------------------------
# LEG GROUPS (TRIPOD GAIT)
# -----------------------------

A = [(L1H, L1K), (L4H, L4K), (L5H, L5K)]
B = [(L2H, L2K), (L3H, L3K), (L6H, L6K)]

# -----------------------------
# BASIC POSTURE
# -----------------------------

def stand():
    for h, k in A + B:
        set_hip(h, CENTER)
        set_knee(k, KNEE_DOWN)

# -----------------------------
# STEP FUNCTION
# -----------------------------

def step(group, opposite, direction):

    # lift tripod
    for h, k in group:
        set_knee(k, KNEE_UP)

    sleep(0.15)

    # swing hips
    for h, k in group:
        set_hip(h, CENTER - HIP_STEP * direction)

    for h, k in opposite:
        set_hip(h, CENTER + HIP_STEP * direction)

    sleep(0.15)

    # lower tripod
    for h, k in group:
        set_knee(k, KNEE_DOWN)

    sleep(0.15)

# -----------------------------
# MAIN LOOP
# -----------------------------

print("Starting tripod gait...")

stand()
sleep(2)

while True:
    step(A, B, +1)
    step(B, A, +1)
