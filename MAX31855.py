import time, math
import RPi.GPIO as GPIO
#import numpy

class max31855(object):

	def __init__(self, csPin = 22, misoPin = 9, mosiPin = 10, clkPin = 11):
		self.csPin = csPin
		self.misoPin = misoPin
		self.mosiPin = mosiPin
		self.clkPin = clkPin
		self.setupGPIO()

	def setupGPIO(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.csPin, GPIO.OUT)
		GPIO.setup(self.misoPin, GPIO.IN)
		GPIO.setup(self.mosiPin, GPIO.OUT)
		GPIO.setup(self.clkPin, GPIO.OUT)

		GPIO.output(self.csPin, GPIO.HIGH)
		GPIO.output(self.clkPin, GPIO.LOW)
		GPIO.output(self.mosiPin, GPIO.LOW)

	def readTemp(self):
		out = self.readRegisters(0,4)
		temp = (out[0] << 24 | out[1] << 16) >> 18
		temp = temp * .25
		temp = ((temp * (9/5)) + 32)
		return temp + 16

	def writeRegister(self, regNum, dataByte):
		GPIO.output(self.csPin, GPIO.LOW)

		# 0x8x to specify 'write register value'
		addressByte = 0x80 | regNum;
		# first byte is address byte
		self.sendByte(addressByte)
		# the rest are data bytes
		self.sendByte(dataByte)

		GPIO.output(self.csPin, GPIO.HIGH)

	def readRegisters(self, regNumStart, numRegisters):
		out = []
		GPIO.output(self.csPin, GPIO.LOW)

		for byte in range(numRegisters):
			data = self.recvByte()
			out.append(data)

		GPIO.output(self.csPin, GPIO.HIGH)
		return out

	def sendByte(self,byte):
		for bit in range(8):
			GPIO.output(self.clkPin, GPIO.HIGH)
			if (byte & 0x80):
				GPIO.output(self.mosiPin, GPIO.HIGH)
			else:
				GPIO.output(self.mosiPin, GPIO.LOW)
			byte <<= 1
			GPIO.output(self.clkPin, GPIO.LOW)

	def recvByte(self):
		byte = 0x00
		for bit in range(8):
			GPIO.output(self.clkPin, GPIO.HIGH)
			byte <<= 1
			if GPIO.input(self.misoPin):
				byte |= 0x1
			GPIO.output(self.clkPin, GPIO.LOW)
		return byte


class FaultError(Exception):
	pass
