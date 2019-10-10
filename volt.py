from ina219 import INA219
from ina219 import DeviceRangeError
from time import sleep
import pygsheets
import datetime

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 2.0
ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V)

c = pygsheets.authorize()
s = c.open('Example solar calcs')
ws = s.worksheet('title', 'real_data')

def read_ina219():
    try:
        ws.append_table([str(datetime.datetime.now()), '{0:0.2f}'.format(ina.voltage()), '{0:0.2f}'.format(ina.current()), '{0:0.2f}'.format(ina.voltage() * ina.current())], start='A1', end=None, dimension='ROWS', overwrite=False)
        # ws.append_table(['{0:0.2f}'.format(ina.voltage())], start='B1', end=None, dimension='ROWS', overwrite=False)
        # ws.append_table(['{0:0.2f}'.format(ina.current())], start='C1', end=None, dimension='ROWS', overwrite=False)
        # ws.append_table(['{0:0.2f}'.format(ina.voltage() * ina.current())], start='D1', end=None, dimension='ROWS', overwrite=False)
        print('Bus Voltage: {0:0.2f}V'.format(ina.voltage()))
        print('Bus Current: {0:0.2f}mA'.format(ina.current()))
        print('Power: {0:0.2f}mW'.format(ina.voltage() * ina.current()))
        print('Shunt Voltage: {0:0.2f}mV\n'.format(ina.shunt_voltage()))
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resister
        print(e)

while 1:
    read_ina219()
    sleep(1)
