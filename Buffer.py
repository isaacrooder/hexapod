import libary
import pigpio
from time import sleep

pi = pigpio.pi()
base = libary.Servo(pi, 18)
hip = libary.Servo(pi, 4)
basetwo = libary.Servo(pi, 27)
hiptwo = libary.Servo(pi, 2)

legtwo = libary.Leg(hiptwo, basetwo)
leg = libary.Leg(hip, base)
def movesetone(leg, legtwo):
	leg.liftleft()
	legtwo.liftright()
	sleep(1)
	leg.forwardleft()
	legtwo.forwardright()
	sleep(1)
	leg.lowerleft()
	legtwo.lowerright
	sleep(1)
	leg.centerleft()
	legtwo.centerright()
	
	sleep(1)

while True:
	movesetone(leg, legtwo)
	sleep(1)




