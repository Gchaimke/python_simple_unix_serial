#!/usr/bin/python

import serial, time
#initialization and open the port

#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

ser = serial.Serial()
ser.port = "/dev/ttyS1"
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
#ser.timeout = None          #block read
ser.timeout = 1            #non-block read
#ser.timeout = 2              #timeout block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2     #timeout for write

try: 
    ser.open()
except Exception as e:
    print (f"error open serial port: {e}")
    exit()

if ser.isOpen():
    try:
        ser.flushInput() #flush input buffer, discarding all its contents
        ser.flushOutput()#flush output buffer, aborting current output 
                        #and discard all that is in buffer
        #write data
        dataS = "\x81\xD2"
        ser.write(dataS)
        print(f"write data: {dataS}")
        time.sleep(0.5)  #give the serial port sometime to receive the data
        response = ser.readline().encode('hex')
        response = response[4:12]
        batVolt =response[2:4]+""+response[0:2]
        batVolt = int(batVolt,16)
        batVolt = str(batVolt)
        batVolt = batVolt[0:2]+","+batVolt[2:5]
        batTem = response[4:6]
        batCur = response[6:8]
        print(f"Battery voltage: {batVolt}V")
        print(f"Battery temperature: {batTem}C")
        print(f"Battery capacity: {batCur}%")
        ser.close()
    except Exception as e:
        print(f"error communicating...: {e}" )
else:
    print("cannot open serial port ")