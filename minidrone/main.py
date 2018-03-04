import cv2
import logging
import threading
import time
from pynput import keyboard
from controller import SumoController

class Main:

    
    
    def main(self):
    
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.speed = 0
        self.turn = 0
    
        self.ctrl = SumoController()
        self.ctrl.connect()
        print('starting...')
        self.ctrl.volume(100)
        self.ctrl.requestAllStates()
        # Collect events until released
        with keyboard.Listener( on_press=self.on_press, on_release=self.on_release) as listener:
            threading.Timer(0.01,self.task).start()
            threading.Timer(10,self.displayBatteryLevel).start()
            listener.join()
            
                
    def displayBatteryLevel(self):           
        print ('{}%'.format(self.ctrl.BatteryLevel()))
        self.ctrl.requestAllStates()	
        threading.Timer(10,self.displayBatteryLevel).start()
    
    def task(self):
        mod = 0;
        ACCELERATION_CONSTANT=10
        DECCELERATION_CONSTANT=5
        TURN_CONSTANT = 2
        if self.up==True:
            if self.speed >= 0:
                mod = ACCELERATION_CONSTANT
            else: #breaking - we are going reverse 
                mod = ACCELERATION_CONSTANT * 2        
        elif self.down==True:
            if self.speed <= 0:
                mod = -ACCELERATION_CONSTANT
            else: #breaking 
                mod = -ACCELERATION_CONSTANT * 2
        else:
            mod = -(self.speed//DECCELERATION_CONSTANT); #/* the faster we go the more we reduce speed */
            if (mod == 0 and self.speed):
                if self.speed < 0:
                    mod = 1 
                else:
                    mod = -1
    
        self.speed += mod;
        
        if self.speed > 127:
            self.speed = 127
        if self.speed < -127:
            self.speed = -127
        
        #/* turning */        
        mod = 0;
        if self.left==True:
            mod = -TURN_CONSTANT
        elif self.right==True:
            mod = TURN_CONSTANT
        else:
            mod = -self.turn//TURN_CONSTANT * 3
            if (abs(self.turn) < TURN_CONSTANT and self.turn):
                mod = -self.turn
        
        self.turn += mod;
        if self.turn > 32:
            self.turn = 32
        if self.turn < -32:
            self.turn = -32
        
        #print(speed, turn, mod)
        self.ctrl.move(self.speed, self.turn)
        threading.Timer(0.01,self.task).start()

    def on_press(self,key):
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
            # param = enum[stop, spin, tap, slowshake, metronome, oudulation, spinjump, spintoposture, spiral,slalom]
            if key.char=='1': 
                self.ctrl.animation(2) #tap
            elif key.char=='2': 
                self.ctrl.animation(5) #metronome        
            elif key.char=='3': 
                self.ctrl.animation(3) #metronome            
                
        except AttributeError:        
            if key==keyboard.Key.up:
                self.up=True;
            elif key==keyboard.Key.down:
                self.down=True;
            elif key==keyboard.Key.left:
                self.left=True;
            elif key==keyboard.Key.right:
                self.right=True;
            elif key==keyboard.Key.space:
                self.ctrl.turn(3) # +180

    def on_release(self,key):  
        if key == keyboard.Key.esc:        
            return False
        if key==keyboard.Key.up:
            self.up=False;
        elif key==keyboard.Key.down:
            self.down=False;
        elif key==keyboard.Key.left:
            self.left=False;
        elif key==keyboard.Key.right:
            self.right=False;
    

if __name__ == '__main__':
    logging.basicConfig(filename='sumo.log', level=logging.INFO)
    objName = Main()
    objName.main()     
