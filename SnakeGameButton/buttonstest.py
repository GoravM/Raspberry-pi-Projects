from signal import pause
from gpiozero import Button
from time import sleep

#initialize buttons and their respective gpio pins
upbutton =  Button(23)
rightbutton = Button(18)
leftbutton = Button(27)
downbutton = Button(17)
endbutton = Button(24)

try: 
    while(True):
    	#when you press the buttons the value changes from 0 to 1
        print(f"up: {upbutton.value},right: {rightbutton.value},left: {leftbutton.value},down: {downbutton.value},end: {endbutton.value}")
        
        sleep(0.1)
	
except KeyboardInterrupt:
    pass

finally:
    
    upbutton.close()
    rightbutton.close()
    leftbutton.close()
    downbutton.close()
    endbutton.close()
