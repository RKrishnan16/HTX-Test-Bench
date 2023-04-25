#!/usr/bin/env python3
import minimalmodbus


instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # port name, slave address (in decimal)
instrument.serial.baudrate = 9600 # set baud rate
instrument.debug = True
instrument.serial.bytesize = 8
# SP1 (SetPoint) = Hex 007F = 127 Dec

## Read temperature (PV = ProcessValue) ##
#instrument.write_register(127,23, 1)  # Registernumber OO1C HEX = 28 Decimal, number of decimals
try:
    instrument.write_register(127,25,1)
except minimalmodbus.InvalidResponseError:
    pass
