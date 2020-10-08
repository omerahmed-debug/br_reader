from br_reader_app.models import Reading
import serial
import time
import sys

class Capture:
    ser = ''
    # add to cron job to read every 15 minutes
    # */15 * * * * /bin/bash -l -c 'cd /home/pi/Desktop/br_reader/ && python3 manage.py read_and_save'

    def init(self):
        # open serial device connection
        port = '/dev/ttyUSB0'
        self.ser = serial.Serial(port, baudrate=9600, bytesize=serial.EIGHTBITS,
                            timeout=16, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE, rtscts=0, dsrdtr=0)

        print("Current port: " + self.ser.name + "\n" + str(self.ser.get_settings()))
        
        # allow time for initial input to load from barometer
        self.sleep("15 Seconds delay", 15.5)

    def read(self):
        # first initialize the connection
        self.init()
        ret_val = {'Pressure': 0, 'Humidity': 0, 'Temprature': 0}
        
        # Read data: Usage- Cmd Line: 26 bytes
        line = self.ser.read(26)
        print(line)

        # Close serial connection
        self.ser.close()
        
        # Parse the input
        line = str(line)
        datalist = line.split(",")

        # Quickly check if input is read correctly
        if datalist[0] == 'b\'P' or datalist[0] == 'b\'\\x00P' or datalist[0] == 'b\'\\rP':
            ret_val['Pressure'] = int(datalist[2])
            ret_val['Humidity'] = str(datalist[4])
            ret_val['Temprature'] = float((datalist[6])[:6])
        
        # Display readings
        print(ret_val)
        return ret_val

    def read_and_save(self):
        print('Reading . . .')
        read_value = self.read()
        print('Saving . . .')
        reading = Reading()
        reading.pressure = float(read_value['Pressure'])
        reading.humidity = float(read_value['Humidity'])
        reading.temprature = float(read_value['Temprature'])
        reading.save()

    def sleep(self, msg, length):
        counter = 0
        index = 0
        spinner = ["|","/","-","\\","-"]
        while (counter < length):
            print(msg + " [" + spinner[index % 4] + "] ", end='\r')
            time.sleep(0.1)
            counter += 0.1
            index += 1
        print(msg + " : Delay complete")