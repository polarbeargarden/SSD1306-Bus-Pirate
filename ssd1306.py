import serial
import random
from time import sleep

global ser
ser = serial.Serial('COM3',115200) # Edit COM number to match your Bus Pirate
global i2caddr
i2caddr = bytes('0x78','utf-8') # Make sure this matches the i2c address of your SSD1306
global col
global row

alphabet = {
    'A':'0x0 0x7c 0x12 0x11 0x12 0x7c 0x0',
    'B':'0x0 0x7f 0x49 0x49 0x49 0x36 0x0',
    'C':'0x0 0x3e 0x41 0x41 0x41 0x22 0x0',
    'D':'0x0 0x7f 0x41 0x41 0x41 0x3e 0x0',
    'E':'0x0 0x7f 0x49 0x49 0x49 0x41 0x0',
    'F':'0x0 0x7f 0x9 0x9 0x9 0x1 0x0',
    'G':'0x0 0x3e 0x41 0x49 0x49 0x3a 0x0',
    'H':'0x0 0x7f 0x8 0x8 0x8 0x7f 0x0',
    'I':'0x0 0x41 0x41 0x7f 0x41 0x41 0x0',
    'J':'0x0 0x30 0x40 0x40 0x40 0x3f 0x0',
    'K':'0x0 0x7f 0x8 0x14 0x22 0x41 0x0',
    'L':'0x0 0x7f 0x40 0x40 0x40 0x40 0x0',
    'M':'0x0 0x7f 0x2 0x4 0x2 0x7f 0x0',
    'N':'0x0 0x7f 0x6 0x8 0x30 0x7f 0x0',
    'O':'0x0 0x3e 0x41 0x41 0x41 0x3e 0x0',
    'P':'0x0 0x7f 0x9 0x9 0x9 0x6 0x0',
    'Q':'0x0 0x3e 0x41 0x51 0x21 0x5e 0x0',
    'R':'0x0 0x7f 0x19 0x19 0x29 0x46 0x0',
    'S':'0x0 0x26 0x49 0x49 0x49 0x32 0x0',
    'T':'0x0 0x1 0x1 0x7f 0x1 0x1 0x0',
    'U':'0x0 0x3f 0x40 0x40 0x40 0x3f 0x0',
    'V':'0x0 0x1f 0x20 0x40 0x20 0x1f 0x0',
    'W':'0x0 0x7f 0x20 0x10 0x20 0x7f 0x0',
    'X':'0x0 0x63 0x14 0x8 0x14 0x63 0x0',
    'Y':'0x0 0x3 0x4 0x78 0x4 0x3 0x0',
    'Z':'0x0 0x61 0x51 0x49 0x45 0x43 0x0',
    '1':'0x0 0x40 0x42 0x7f 0x40 0x40 0x0',
    '2':'0x0 0x42 0x61 0x51 0x49 0x46 0x0',
    '3':'0x0 0x22 0x41 0x49 0x49 0x36 0x0',
    '4':'0x0 0xf 0x8 0x8 0x8 0x7f 0x0',
    '5':'0x0 0x27 0x45 0x45 0x45 0x39 0x0',
    '6':'0x0 0x3e 0x49 0x49 0x49 0x32 0x0',
    '7':'0x0 0x1 0x1 0x71 0xd 0x3 0x0',
    '8':'0x0 0x36 0x49 0x49 0x49 0x36 0x0',
    '9':'0x0 0x26 0x49 0x49 0x49 0x3e 0x0',
    '0':'0x0 0x3e 0x71 0x5d 0x47 0x3e 0x0',
    ':':'0x0 0x0 0x0 0x22 0x0 0x0 0x0',
    ' ':'0x0 0x0 0x0 0x0 0x0 0x0 0x0',
    ',':'0x0 0x40 0x30 0x0 0x0 0x0 0x0',
    '!':'0x0 0x0 0x6f 0x0 0x0 0x0 0x0',
    '?':'0x0 0x6 0x1 0x51 0x9 0x6 0x0',
    '.':'0x0 0x0 0x40 0x0 0x0 0x0 0x0'
}

# This sends commands to the Bus Pirate
def buspirate_cmd(cmd):
    bcmd = bytes(cmd,'utf-8')
    ser.write(bcmd+b'\r')
    sleep(0.5)

# This sends commands to your SSD1306
def ssd1306_cmd(cmd):
    bcmd = bytes(cmd,'utf-8')
    ser.write(b'['+i2caddr+b' 0x00 '+bcmd+b']\r')
    sleep(0.01)
    
# This sends screen control instructions to your SSD1306
def ssd1306_ctrl(cmd):
    bcmd = bytes(cmd,'utf-8')
    ser.write(b'['+i2caddr+b' 0x40 '+bcmd+b']\r')
    sleep(0.01)
    
# This initializes the SSD1306
def ssd1306_init():
    buspirate_cmd('m') #BP Mode Select
    buspirate_cmd('4') #Select I2C
    buspirate_cmd('2') #Speed 50khz (1=5khz, 2=50khz, 3=100khz, 4=400khz. All work with ssd1306)
    buspirate_cmd('W') #Enable BP power supplies
    buspirate_cmd('P') #Enable BP pullup resistors
    ssd1306_cmd('0xae') #Display off
    ssd1306_cmd('0xd5') #Set display clock div
    ssd1306_cmd('0x80') #Suggested ratio
    ssd1306_cmd('0xa8') #Set multiplex
    ssd1306_cmd('0x3f') #
    ssd1306_cmd('0xd3') #Set display offset
    ssd1306_cmd('0x00') #No offset
    ssd1306_cmd('0x40') #Set startline = 0 (0x40 | 0x00)
    ssd1306_cmd('0x8d') #Charge pump
    ssd1306_cmd('0x14') #Set non-external VCC for charge pump
    ssd1306_cmd('0x20') #Memory mode
    ssd1306_cmd('0x00') #act like ks0108?
    ssd1306_cmd('0xa1') #Segremap | 0x01
    ssd1306_cmd('0xc8') #comscandec
    ssd1306_cmd('0xda') #Set com pins
    ssd1306_cmd('0x12') #
    ssd1306_cmd('0x81') #Set contrast
    ssd1306_cmd('0xcf') #Contrast for internal vcc
    ssd1306_cmd('0xd9') #Set precharge
    ssd1306_cmd('0xf1') #Set internal vcc for precharge
    ssd1306_cmd('0xdb') #Set vcom detect
    ssd1306_cmd('0x40') #
    ssd1306_cmd('0xa4') #Display All on resume
    ssd1306_cmd('0xa6') #Normal display
    ssd1306_cmd('0xaf') #Display on

# This preps the screen by defining the entire screen as the working area.
def ssd1306_scr_prep():
    ssd1306_cmd('0x21') #Column address
    ssd1306_cmd('0x00') #Start column 0
    ssd1306_cmd('0x7F') #End column 127
    ssd1306_cmd('0x22') #Page address
    ssd1306_cmd('0x00') #Start page 0
    ssd1306_cmd('0x07') #End page 7

#This re-defines the screen area we're interacting with.
def ssd1306_scr_area(col_start, col_end, page_start, page_end):
    ssd1306_cmd('0x21') #Column address
    ssd1306_cmd(col_start) #Start column 0
    ssd1306_cmd(col_end) #End column 127
    ssd1306_cmd('0x22') #Page address
    ssd1306_cmd(page_start) #Start page 0
    ssd1306_cmd(page_end) #End page 7

# This makes it easier to dim the screen, send True to dim or False to un-dim
def ssd1306_dim(tf):
    if(tf):
        contrast = '0x00'
    else:
        contrast = '0xcf'
        
    ssd1306_cmd('0x81')
    ssd1306_cmd(contrast)

# This inverts the screen, like before, True or False.
def ssd1306_invert(tf):
    if(tf):
        ssd1306_cmd('0xA7')
    else:
        ssd1306_cmd('0xA6')

# This starts scrolling the first row.
def ssd1306_scrollright():
    ssd1306_cmd('0x26'); #Right horizontal scroll
    ssd1306_cmd('0x00');
    ssd1306_cmd('0x00'); #Start row
    ssd1306_cmd('0x00');
    ssd1306_cmd('0x01'); #Stop row
    ssd1306_cmd('0x00');
    ssd1306_cmd('0xff');
    ssd1306_cmd('0x2f'); #Activate scroll
        
# This sets screen brightness.
def ssd1306_brightness(value):
    ssd1306_cmd('0x81');
    ssd1306_cmd(value);

#def ssd1306_print(str_array):
#    for i in str_array:
#        ssd1306_ctrl(i)
#        sleep(0.05)

# This prints text from the alphabet array above.
def ssd1306_print(string):
    global col
    global row
    for i in string:
        if (col >= 18):
            row = (row + 1) % 7
            ssd1306_scr_area('0x01','0x7f',hex(row),hex(row))
            col = 0
        ssd1306_ctrl(alphabet[i])
        
        col = col + 1
        sleep(0.05)

# This prints text form the alphabet above and advances to the next line.
def ssd1306_println(string):
    global col
    global row
    for i in string:
        if (col >= 18):
            row = (row + 1) % 7
            ssd1306_scr_area('0x01','0x7f',hex(row),hex(row))
            col = 0
        ssd1306_ctrl(alphabet[i])
        col = col + 1
        sleep(0.05)
    row = row + 1
    ssd1306_scr_area('0x01','0x7f',hex(row),hex(row))
    col = 0

# Main method, this initializes the screen and fills it.    
def main():
    ssd1306_init()
    ssd1306_scr_prep()
    ssd1306_ctrl('0xff:1024')  #Fill screen

main()
sleep(1)


# Uncomment this block to fill parts of the screen with random dots.
#ssd1306_scr_area(31,94,3,4)
#sleep(1)
#for i in range(128):
#    tmp = random.randrange(1,255)
#    ssd1306_ctrl(hex(tmp))
#sleep(1)


ssd1306_ctrl('0x00:1024') #Empty screen
sleep(1)
#ssd1306_scr_area('0x01','0x7e', '0x00', '0x00')
col = 0
row = 0
sleep(0.5)
for i in range(1):
    ssd1306_println('HELLO WORLD! ')
    ssd1306_println('THIS IS SSD1306')
    ssd1306_println('')
    ssd1306_println('BUS PIRATE TEST')
    ssd1306_println('')
    ssd1306_println('')
    #ssd1306_println('.')
    #ssd1306_println('.')



#for i in range(1024):
#    ssd1306_ctrl(hex(random.randrange(1,255)))
#sleep(1)

#for i in range(100):
#    startcol=random.randrange(0,126)
#    page=random.randrange(0,7)
#    ssd1306_scr_area(startcol,startcol+1,page,page)
#    ssd1306_ctrl(hex(random.randrange(1,255)))

#ssd1306_dim(True)
print('Complete')
