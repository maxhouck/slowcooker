import MAX31855
csPin =22
misoPin = 9
mosiPin = 10
clkPin = 11
max = MAX31855.max31855(csPin,misoPin,mosiPin,clkPin)
temp = max.readTemp()
print(temp)
