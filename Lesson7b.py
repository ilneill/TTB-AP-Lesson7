# Using an Arduino with Python LESSON 7: Measuring Temperature and Humidity With the DHT11.
# https://www.youtube.com/watch?v=kF6biceKwFY
# https://toptechboy.com/using-an-arduino-with-python-lesson-7-measuring-temperature-and-humidity-with-the-dht11/

# Internet References:
# https://www.glowscript.org/docs/VPythonDocs/index.html

import time
import serial
from vpython import *
import numpy as np

# vPython refresh rate.
vPythonRefreshRate = 100
# Helper Scale Axis toggle.
showAxis = False
# Test the meters with pseudo random data.
pseudoDataMode = False

# A place to put our things...
canvas(title = "<b><i>Arduino with Python - Real World Measurements Visualised!</i></b>", background = color.cyan, width = 800, height = 600)

if showAxis:
    # X-Origin.
    arrow(color = color.blue , round = True, pos = vector(-0.5, 0, 0), axis = vector(1, 0, 0), shaftwidth = 0.02)
    # Y-Origin.
    arrow(color = color.blue, round = True, pos = vector(0, -0.5, 0), axis = vector(0, 1, 0), shaftwidth = 0.02)
    # Z-Origin.
    arrow(color = color.blue, round = True, pos = vector(0, 0, -0.5), axis = vector(0, 0, 1), shaftwidth = 0.02)
    # X-Axis.
    for graduation in range(6):
        arrow(color = color.magenta, round = True, pos = vector(graduation / 2, 0, 0.25), axis = vector(0.5, 0, 0), shaftwidth = 0.02)
        arrow(color = color.magenta, round = True, pos = vector(-graduation / 2, 0, 0.25), axis = vector(-0.5, 0, 0), shaftwidth = 0.02)
    # Y-Axis.
    for graduation in range(4):
        arrow(color = color.magenta, round = True, pos = vector(0, graduation / 2, 0.25), axis = vector(0, 0.5, 0), shaftwidth = 0.02)
        arrow(color = color.magenta, round = True, pos = vector(0, -graduation / 2, 0.25), axis = vector(0, -0.5, 0), shaftwidth = 0.02)
    # Z-Axis.
    for graduation in range(2):
        arrow(color = color.magenta, round = True, pos = vector(0, 0, graduation / 2), axis = vector(0, 0, 0.5), shaftwidth = 0.02)
        arrow(color = color.magenta, round = True, pos = vector(0, 0, -graduation / 2), axis = vector(0, 0, -0.5), shaftwidth = 0.02)

# Return some pseudo data for meter testing.
def pseudoData():
    time.sleep(0.1) # Not too fast...
    pot1Value = int(1023 * np.random.rand())
    tDHT11 = (80 * np.random.rand() - 10.0)
    hDHT11 = (100 * np.random.rand())
    tDHT22 = (80 * np.random.rand() - 10.0)
    hDHT22 = (100 * np.random.rand())
    return(pot1Value, tDHT11, hDHT11, tDHT22, hDHT22)

# Draw small screw exactly where we like.
def drawScrew(sPos = vector(0, 0, 0)):
    cylinder(color = color.black, opacity = 1, pos = vector(0, 0, 0.05) + sPos, axis = vector(0, 0, 0.04), radius = 0.06) # Head.
    cylinder(color = color.black, opacity = 1, pos = vector(0, 0, 0) + sPos, axis = vector(0, 0, 0.05), radius = 0.03) # Shaft.
    cone(color = color.black, opacity = 1, pos = vector(0, 0, 0) + sPos, axis = vector(0, 0, -0.25), radius = 0.03) # Thread.
    slotAngle = np.random.rand() * np.pi / 2 # An angle between 0 and 90 degrees.
    screwCross1 = box(color = vector(0.8, 0.8, 0.8), opacity = 1, pos = vector(0, 0, 0.0801) + sPos, size = vector(0.1, 0.02, 0.02)) # Cross pt1.
    screwCross1.rotate(angle = slotAngle, axis = vector(0, 0, 1))
    screwCross2 = box(color = vector(0.8, 0.8, 0.8), opacity = 1, pos = vector(0, 0, 0.0801) + sPos, size = vector(0.1, 0.02, 0.02)) # Cross pt2.
    screwCross2.rotate(angle = slotAngle + np.pi / 2, axis = vector(0, 0, 1)) # Add 90 degrees for the other part of the cross.

# Draw a meter - Type 1.
class meterType1:
    def __init__(self, mt1Pos = vector(0, 0, 0), mt1Color = color.red, mt1ScaleMin = 0, mt1ScaleMax = 100, mt1Label = "", mt1Units = ""):
        self.mt1Pos = mt1Pos
        self.mt1Color = mt1Color
        self.mt1ScaleMin = mt1ScaleMin
        self.mt1ScaleMax = mt1ScaleMax
        self.mt1Label = mt1Label
        self.mt1Units = mt1Units
        # Draw the meter...
        box(color = color.white, opacity = 1, size = vector(2.5, 1.5, 0.1), pos = vector(0, 0, 0) + self.mt1Pos) # Draw the meter box.
        # Draw the meter needle and set it to the 0 position.
        self.meterNeedle = arrow(length = 1, shaftwidth = 0.02, color = self.mt1Color, round = True, pos = vector(0, -0.65, 0.1) + self.mt1Pos, axis = vector(np.cos(5 * np.pi / 6), np.sin(5 * np.pi / 6), 0))
        sphere(radius = 0.05, color = self.mt1Color, pos = vector(0, -0.65, 0.1) + self.mt1Pos)
        cylinder(color = color.gray(0.5), pos = vector(0, -0.5, 0.05) + self.mt1Pos, axis = vector(0, 0, 0.01), radius = 0.2)
        # Draw the meter scale major marks.
        for unitCounter, theta in zip(range(6), np.linspace(5 * np.pi / 6, np.pi / 6, 6)):
            majorUnit = text(text = str(unitCounter), color = self.mt1Color, opacity = 1, align = "center", height = 0.1, pos = vector(1.1 * np.cos(theta), 1.1 * np.sin(theta) - 0.65, 0.095) + self.mt1Pos)
            majorUnit.rotate(angle = theta - np.pi / 2, axis = vector(0, 0, 1))
            box(color = color.black, pos = vector(np.cos(theta), np.sin(theta) - 0.65, 0.08) + self.mt1Pos, size = vector(0.1, 0.02, 0.02), axis = vector(np.cos(theta), np.sin(theta), 0))
        # Draw the meter scale minor marks.
        for unitCounter, theta in zip(range(51), np.linspace(5 * np.pi / 6, np.pi / 6, 51)):
            if unitCounter % 5 == 0 and unitCounter % 10 != 0:
                minorUnit = text(text = "5", color = self.mt1Color, opacity = 1, align = "center", height = 0.05, pos = vector(1.05 * np.cos(theta), 1.05 * np.sin(theta) - 0.65, 0.095) + self.mt1Pos)
                minorUnit.rotate(angle = theta - np.pi / 2, axis = vector(0, 0, 1))
            box(color = color.black, pos = vector(np.cos(theta), np.sin(theta) - 0.65, 0.08) + self.mt1Pos, size = vector(0.05, 0.01, 0.01), axis = vector(np.cos(theta), np.sin(theta), 0))
        # Meter Label and Units.
        text(text = self.mt1Label, color = self.mt1Color, opacity = 1, align = "center", height = 0.1, pos = vector(0, 0.6, 0.1) + self.mt1Pos, axis = vector(1, 0, 0))
        text(text = self.mt1Units, color = self.mt1Color, opacity = 1, align = "center", height = 0.115, pos = vector(0, 0, 0.1) + self.mt1Pos, axis = vector(1, 0, 0))
        # Add a raw reading too.
        self.rawValue = label(text = "0000", color = self.mt1Color, height = 10, opacity = 0, box = False, pos = vector(-0.9, 0.6, 0.1) + self.mt1Pos)
        # Add a digital reading too.
        self.digitalValue = label(text = "0.00V", color = self.mt1Color, height = 10, opacity = 0, box = False, pos = vector(0.9, 0.6, 0.1) + self.mt1Pos)
        # Top Left corner screw.
        drawScrew(vector(-1.17, 0.67, -0.03) + self.mt1Pos)
        # Top Right corner screw.
        drawScrew(vector(1.17, 0.67, -0.03) + self.mt1Pos)
        # Bottom Left corner screw.
        drawScrew(vector(-1.17, -0.67, -0.03) + self.mt1Pos)
        # Bottom Right corner screw.
        drawScrew(vector(1.17, -0.67, -0.03) + self.mt1Pos)
        # Lets put a mostly transparent glass cover over the meter.
        box(color = color.white, opacity = 0.25, size = vector(2.5, 1.5, 0.25), pos = vector(0, 0, 0.15) + self.mt1Pos)
        # At this point we have no data to drive the meter.
        self.DataWarning = text(text = "-No Data-", color = self.mt1Color, opacity = 1, align = "center", height = 0.125, pos = vector(0, -0.25, 0.2) + self.mt1Pos, axis = vector(1, 0, 0))
    def update(self, mt1Value = 0):
        if mt1Value != "-1":
            self.mt1Value = mt1Value
            # Turn off the data warning.
            self.DataWarning.opacity = 0
            # Print the raw potentiometer value.
            self.rawValue.text = str("<i>%04d</i>" % mt1Value)
            # Print the digital voltage.
            voltage = round(5 * mt1Value / 1024, 2)
            self.digitalValue.text = str("%1.2f" % voltage) + "V"
            # Use the potentiometer to set the meter needle angle.
            # How this works:
            #   0V is 5pi/6 rads, 5V is pi/6 rads, thus the needle range is 4pi/6 rads.
            #   The pot range is 0 - 1023, or 1024 steps, so each step is 4pi/6/1024, or pi/1536 rads.
            #   Thus, the needle position is 5pi/6 - (pi/1536 X Potentiometer Value) rads.
            theta = (5 * np.pi / 6) - (np.pi / 1536 * self.mt1Value)
            self.meterNeedle.axis = vector(np.cos(theta), np.sin(theta), 0)
        else:
            # Turn on the data warning.
            self.DataWarning.opacity = 1

# Draw a meter - Type 3.
class meterType3:
    def __init__(self, mt3Pos = vector(0, 0, 0), mt3Color = color.red, mt3ScaleMin = 0, mt3ScaleMax = 100, mt3Label = "", mt3Units = ""):
        self.mt3Pos = mt3Pos
        self.mt3Color = mt3Color
        self.mt3ScaleMin = mt3ScaleMin
        self.mt3ScaleMax = mt3ScaleMax
        self.mt3Label = mt3Label
        self.mt3Units = mt3Units
        self.mt3Range = mt3ScaleMax - mt3ScaleMin
        # Draw the meter...
        box(color = color.white, opacity = 1, size = vector(0.75, 1.75, 0.1), pos = vector(0, 0, 0) + self.mt3Pos)
        sphere(color = self.mt3Color, radius = 0.1, pos = vector(0, -0.65, 0.15) + self.mt3Pos)
        cylinder(color = color.gray(0.5), opacity = 1, pos = vector(0, -0.65, 0.15) + self.mt3Pos, axis = vector(0, 1.15, 0), radius = 0.049)
        sphere(color = color.gray(0.5), opacity = 1, radius = 0.049, pos = vector(0, 0.5, 0.15) + self.mt3Pos)
        self.measurement = cylinder(color = self.mt3Color, pos = vector(0, -.65, 0.15) + self.mt3Pos, axis = vector(0, 0.15, 0), radius = 0.05)
        for unit, tick in zip(np.linspace(self.mt3ScaleMin, self.mt3ScaleMax, 11), np.linspace(0, 1, 11)):
            text(text = str(unit), color = self.mt3Color, align = "right", height = 0.05, pos = vector(-0.15, -0.6725 + 0.15 + tick, 0.15) + self.mt3Pos)
            box(color = color.black, pos = vector(-0.1, -0.65 + 0.15 + tick, 0.15) + self.mt3Pos, size = vector(0.05, 0.01, 0.01), axis = vector(1, 0, 0))
        for tick in np.linspace(0, 1, 51):
            box(color = color.black, pos = vector(-0.1, -0.65 + 0.15 + tick, 0.15) + self.mt3Pos, size = vector(0.025, 0.005, 0.005), axis = vector(1, 0, 0))
        text(text = self.mt3Label, color = self.mt3Color, opacity = 1, align = "center", height = 0.075, pos = vector(0, 0.6, 0.15) + self.mt3Pos, axis = vector(1, 0, 0))
        text(text = self.mt3Units, color = self.mt3Color, opacity = 1, align = "left", height = 0.095, pos = vector(0.125, -0.685, 0.15) + self.mt3Pos, axis = vector(1, 0, 0))
        # Add a raw reading too.
        self.rawValue = label(text = "00.0", color = self.mt3Color, height = 10, opacity = 0, box = False, pos = vector(0, -0.82, 0.1) + self.mt3Pos)
        # Top Left corner screw.
        drawScrew(vector(-0.3, 0.8, -0.03) + self.mt3Pos)
        # Top Right corner screw.
        drawScrew(vector(0.3, 0.8, -0.03) + self.mt3Pos)
        # Bottom Left corner screw.
        drawScrew(vector(-0.3, -0.8, -0.03) + self.mt3Pos)
        # Bottom Right corner screw.
        drawScrew(vector(0.3, -0.8, -0.03) + self.mt3Pos)
        # Lets put a mostly transparent glass cover over the meter.
        box(color = color.white, opacity = 0.25, size = vector(0.75, 1.75, 0.32), pos = vector(0, 0, 0.1) + self.mt3Pos)
        # At this point we have no data to drive the meter.
        self.DataWarning = text(text = "-No Data-", color = self.mt3Color, opacity = 1, align = "center", height = 0.125, pos = vector(0, 0, 0.2) + self.mt3Pos, axis = vector(1, 0, 0))
    def update(self, mt3Value = 0):
        if mt3Value != "nan":
            self.mt3Value = mt3Value
            # Turn off the data warning.
            self.DataWarning.opacity = 0
            # Print the raw sensor value.
            self.rawValue.text = str("<i>%2.1f</i>" % mt3Value)
            # Update the meter reading.
            self.measurement.axis = vector(0, 0.15 + ((self.mt3Value - self.mt3ScaleMin)  / self.mt3Range), 0)
        else:
            # Turn on the data warning.
            self.DataWarning.opacity = 1

standardMeter1 = meterType1(vector(0, 0.675, -0.1), color.red, 0, 5, "Potentiometer 1", "V")
thermometer1 = meterType3(vector(-2.5, 0.75, -0.1), color.red,- 10, 60, "DHT11 Temp", u"\N{DEGREE SIGN}C")
humiditymeter1 = meterType3(vector(-2.5, -1.25, -0.1), color.blue, 0, 100, "DHT11 Hum", "%")
thermometer2 = meterType3(vector(2.5, 0.75, -0.1), color.red, -10, 60, "DHT22 Temp", u"\N{DEGREE SIGN}C")
humiditymeter2 = meterType3(vector(2.5, -1.25, -0.1), color.blue, 0, 100, "DHT22 Hum", "%")

# Now lets stamp my logo and name on the display... and "EasiFace" is my logo - you need your own!
myLogoL1 = "EasiFace"
for letterCounter, theta in zip(range(len(myLogoL1)), np.linspace(5 * np.pi / 8, 3 * np.pi / 8, len(myLogoL1))):
    logo1Letter = myLogoL1[letterCounter]
    logo1Character = text(text = logo1Letter, color = color.green, opacity = 1, align = "center", height = 0.2, pos = vector(2.1 * np.cos(theta), 2.1 * np.sin(theta) - 3, -0.035), axis = vector(1, 0, 0))
    logo1Character.rotate(angle = theta - np.pi / 2, axis = vector(0, 0, 1))
myLogoL2 = "MeterPanel"
for letterCounter, theta in zip(range(len(myLogoL2)), np.linspace(5 * np.pi / 8, 3 * np.pi / 8, len(myLogoL2))):
    logo2Letter = myLogoL2[letterCounter]
    logo2Character = text(text = logo2Letter, color = color.green, opacity = 1, align = "center", height = 0.2, pos = vector(1.9 * np.cos(theta), 1.8 * np.sin(theta) - 3, -0.035), axis = vector(1, 0, 0))
    logo2Character.rotate(angle = theta - np.pi / 2, axis = vector(0, 0, 1))

# Finally, lets mount it all on a gray metal panel.
box(color = color.gray(0.5), texture = textures.metal, size = vector(7, 4.5, 0.1), pos = vector(0, -0.25, -0.2))
drawScrew(vector(-3.4, 1.9, -0.23))
drawScrew(vector(3.4, 1.9, -0.23))
drawScrew(vector(-3.4, -2.4, -0.23))
drawScrew(vector(3.4, -2.4, -0.23))

# Connect to the Arduino on the correct serial port!
if not pseudoDataMode: # We are not meter testing with pseudo data mode.
    serialOK = True
    try:
        # My Arduino happens to connect as serial port 'com3'. Yours may be different!
        arduinoDataStream = serial.Serial('com3', 115200)
        # Give the serial port time to connect.
        time.sleep(1)
    except serial.SerialException as err:
        serialOK = False
        # Put an error message on top of the meter.
        serialErrorVisible = 0
        serialError = text(text = "-Serial Error-", color = color.red, opacity = serialErrorVisible, align = "center", height = 0.5, pos = vector(0, 0, 0.25), axis = vector(1, 0, 0))
        print("Serial Error: %s." % (str(err)[0].upper() + str(err)[1:])) # A cosmetic fix to uppercase the first letter of err.

# An infinite loop...
while True:
    # Set the vPython refresh rate.
    rate(vPythonRefreshRate)
    if not pseudoDataMode: # We are not meter testing with pseudo data mode.
        if serialOK:
            # Wait until data has been received from the Arduino.
            while arduinoDataStream.in_waiting == 0:
                pass
            # Read the CSV data from the Arduino.
            arduinoDataPacket = arduinoDataStream.readline()
            # Convert the CSV data from a byte stream to a string.
            arduinoDataPacket = str(arduinoDataPacket, 'utf-8')
            # Strip the CRLF from the end of the CSV string.
            arduinoDataPacket = arduinoDataPacket.strip('\r\n')
            # Convert the CSV string into separate variables.
            (pot1Value, tDHT11, hDHT11, tDHT22, hDHT22) = arduinoDataPacket.split(",")
            # Check the returned data and convert the variables to numbers.
            if pot1Value != "-1":
                pot1Value = int(pot1Value)
            if tDHT11 != "nan":
                tDHT11   = float(tDHT11)
            if hDHT11 != "nan":
                hDHT11   = float(hDHT11)
            if tDHT22 != "nan":
                tDHT22   = float(tDHT22)
            if hDHT22 != "nan":
                hDHT22   = float(hDHT22)
        else:
            # Flash the serial error message on top of the meter.
            serialErrorVisible = (serialErrorVisible + 1) % 2 # Using modulo 2 maths to toggle the variable between 0 and 1.
            serialError.opacity = serialErrorVisible
            # Wait for a bit...
            time.sleep(0.5)
    else: # Get some pseudo data to test the meters.
        (pot1Value, tDHT11, hDHT11, tDHT22, hDHT22) = pseudoData()
    # Update the meters.
    standardMeter1.update(pot1Value)
    thermometer1.update(tDHT11)
    humiditymeter1.update(hDHT11)
    thermometer2.update(tDHT22)
    humiditymeter2.update(hDHT22)

# EOF
