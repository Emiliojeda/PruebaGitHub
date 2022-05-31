from math import trunc
import utime
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import machine 
import _thread


I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR,I2C_NUM_ROWS, I2C_NUM_COLS)

sensor_temp = machine.ADC(4)
conversion_factor = 3.3/(65535)
file = open("temps.txt", "w")

buttonT = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)
buttonS = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
buttonD = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN)

global buttonT_pressed
buttonT_pressed = False

global buttonS_pressed
buttonS_pressed = False

global buttonD_pressed
buttonD_pressed = False

def button_reader_thread():
    global buttonT_pressed
    global buttonS_pressed
    global buttonD_pressed
    while True:
        if buttonT.value() == 1:
            buttonT_pressed = True
            buttonS_pressed = False
            buttonD_pressed = False
        utime.sleep_ms(10)
        if buttonS.value() == 1:
            buttonT_pressed = False
            buttonS_pressed = True
            buttonD_pressed = False 
        utime.sleep_ms(10)
        if  buttonD.value() == 1:
            buttonT_pressed = False
            buttonS_pressed = False
            buttonD_pressed = True
        utime.sleep_ms(10)
_thread.start_new_thread(button_reader_thread, ()) 


lcd.move_to(0,0)
lcd.putstr("Welcome")
utime.sleep(5)
lcd.clear()
lcd.move_to(0,0)
lcd.putstr("P1= STR P3= RDY")
lcd.move_to(0,1)
lcd.putstr("P2 = STP!")
while True:
   if buttonT_pressed == True:
       reading = sensor_temp.read_u16()*conversion_factor
       temperature = 25-(reading-0.706)/0.001721
       file.write(str(temperature)+ "\n")
       lcd.clear()
       lcd.move_to(0,0)
       lcd.putstr("Temperature C")
       lcd.move_to(0,1)
       lcd.putstr(str(temperature))
       utime.sleep(5)
   if buttonS_pressed == True:
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("stop monitoring")
        utime.sleep(5)
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("P1 = STR")
        lcd.move_to(0,1)
        lcd.putstr("P3 = RDY")
        utime.sleep(5)
   if buttonD_pressed == True:
       file.close()
       lcd.clear
       lcd.move_to(0,0)
       lcd.putstr("Ready to")
       lcd.move_to(0,1)
       lcd.putstr("download")
       utime.sleep(5)
       while True:
           utime.sleep(10)