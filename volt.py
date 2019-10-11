from ina219 import INA219   
from ina219 import DeviceRangeError
from time import sleep
import pygsheets
import datetime

SHUNT_OHMS = 0.1    # get the resister of the sensor
MAX_EXPECTED_AMPS = 2.0     # set max amp
ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)  # set resister and max amp to INA object
ina.configure(ina.RANGE_16V)

c = pygsheets.authorize()       # authorize your google sheet api
# enable google sheet api and save your auth2 in the same folder as this python file
s = c.open('Example solar calcs')   # get the sheet object by sheet title
ws = s.worksheet('title', 'real_data')  # open the worksheet object by worksheet title

def read_ina219():
    try:
        voltage = ina.voltage()   # read the voltage  (v)
        current = ina.current()  # read the current  (ma)
        power = voltage * current / 1000   # calculate the power (v)
        timestamp = str(datetime.datetime.now())   # get the timestamp from datatime lib
        # insert rows to the google sheet, set format of our data
        ws.append_table([timestamp, '{0:0.2f}'.format(voltage), '{0:0.2f}'.format(current), '{0:0.6f}'.format(power)],
                        start='A1', end=None, dimension='ROWS', overwrite=False)
        # ws.append_table(['{0:0.2f}'.format(ina.voltage())], start='B1', end=None, dimension='ROWS', overwrite=False)
        # ws.append_table(['{0:0.2f}'.format(ina.current())], start='C1', end=None, dimension='ROWS', overwrite=False)
        # ws.append_table(['{0:0.2f}'.format(ina.voltage() * ina.current())], start='D1', end=None, dimension='ROWS', overwrite=False)
        print('Bus Voltage: {0:0.2f}V'.format(voltage))
        print('Bus Current: {0:0.2f}mA'.format(current))
        print('calculate Power: {0:0.2f}mW'.format(power))
        print('Sensor Power: {0:0.2f}mW'.format(ina.power()))
        print('Shunt Voltage: {0:0.2f}mV\n'.format(ina.shunt_voltage()))
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resister
        print(e)

while 1:
    read_ina219()
    sleep(1)
