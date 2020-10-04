import serial
import sys
import time
import csv
import schedule
import math
from datetime import date

# query user for capture settings
while True:
    port = '/dev/ttyUSB0'
    runtime = '3650'
    record = 'y'
    if record == 'y':
        datafile = '/home/pi/Desktop/barometer'
    #timestep = '15'
    timestep = '1'
    print("\nPort: " + port + ", Runtime: " + runtime + " day(s), Record: " +
          record + ", Write: " + datafile + ", Timestep : " + timestep + " min(s) ")
    final = 'y'
    if final == 'y':
        break

# open serial device
ser = serial.Serial(port, baudrate=9600, bytesize=serial.EIGHTBITS,
                    timeout=16, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE, rtscts=0, dsrdtr=0)

print("\nCurrent port: " + ser.name + "\n" + str(ser.get_settings()) + "\n\nStarting...")

time.sleep(15.5) # allow time for initial input to load from barometer
count = 0 # entries read
max = math.ceil(int(runtime)*24*60/int(timestep)) # calculate how many entries are needed
table = [None]*(max+1)

today = date.today()
d = today.strftime("%b-%d-%Y")
currentdate = d

def task():
    global count
    global table
    global currentdate
    #line = ser.read_until('\\')
    line = ser.read(26) # Read data: Usage- Cmd Line: 26 bytes
    print(line)
    count += 1
    
    # parse the input
    line = str(line)
    datalist = line.split(",")
    
    pressure = 'Error'
    humidity = 'Error'
    temp = 'Error'
    
    # quickly check if input is read correctly
    if datalist[0] == 'b\'P':
        pressure = str(int(datalist[2]))
        humidity = str(datalist[4])
        temp = str(float((datalist[6])[:6]))
        
    elif datalist[0] == 'b\'\\x00P':
        pressure = str(int(datalist[2]))
        humidity = str(datalist[4])
        temp = str(float((datalist[6])[:6]))
        
    elif datalist[0] == 'b\'\\rP':
        pressure = str(int(datalist[2]))
        humidity = str(datalist[4])
        temp = str(float((datalist[6])[:6]))
    
    else:
        pressure = line  # show what the bad input is
        line = ser.read(28)
    # get the time
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    today = date.today()
    d = today.strftime("%b-%d-%Y")
    
    # start over number of lines read for new day
    if currentdate != d:
        count = 1
        currentdate = d
    
    # store in a table for analysis and export
    table[count-1] = ['ID: ' + str(count),
                      'Pressure: ' + pressure + ' mb',
                      'Humidity: ' + humidity + ' %RH',
                      'Temp: ' + temp + ' C',
                      'Time: ' + current_time]
    
    # print to console
    print("Lines Read: " + str(count) + ", "
    "Pressure: " + pressure + " mb, "
    "Humidity: " + humidity + " %RH, "
    "Temp: " + temp + " degrees C, "
    "Time: " + current_time)
    
    # export data
    if record == 'y':
        with open(datafile + '/barometer-' + d + '.csv', mode='a') as csvfile:
            wr = csv.writer(csvfile)
            wr.writerow(table[count-1])
    
# get first read right awat 
task()

# wait every 15 minutes for the next read
#schedule.every(int(timestep)).minutes.do(task)

#while (count <= max):
#    schedule.run_pending()

print("\nDone")

class Capture
    def read:
        return task()
