import cv2
import logging
import threading
import time
from pynput import keyboard
from controller import SumoController

up=False
down=False
left=False
right=False
speed = 0
turn=0
ACCELERATION_CONSTANT=10
DECCELERATION_CONSTANT=5
TURN_CONSTANT = 2


def main():
    global ctrl
    ctrl = SumoController()
    ctrl.connect()
    print('starting...')
    # Collect events until released
    with keyboard.Listener( on_press=on_press, on_release=on_release) as listener:
        try:
            threading.Timer(0.01,task).start()
            listener.join()
        except:
            print('error')


def task():
    global ctrl
    global speed, turn
    mod = 0;

    if up==True:
        if speed >= 0:
            mod = ACCELERATION_CONSTANT
        else: #breaking - we are going reverse 
            mod = ACCELERATION_CONSTANT * 2        
    elif down==True:
        if speed <= 0:
            mod = -ACCELERATION_CONSTANT
        else: #breaking 
            mod = -ACCELERATION_CONSTANT * 2
    else:
        mod = -(speed//DECCELERATION_CONSTANT); #/* the faster we go the more we reduce speed */
        if (mod == 0 and speed):
            if speed < 0:
                mod = 1 
            else:
                mod = -1

    speed += mod;
    
    if speed > 127:
        speed = 127
    if speed < -127:
        speed = -127
    
    #/* turning */        
    mod = 0;
    if left==True:
        mod = -TURN_CONSTANT
    elif right==True:
        mod = TURN_CONSTANT
    else:
        mod = -turn//TURN_CONSTANT * 3
        if (abs(turn) < TURN_CONSTANT and turn):
            mod = -turn
    
    turn += mod;
    if turn > 32:
        turn = 32
    if turn < -32:
        turn = -32
    
    #print(speed, turn, mod)
    ctrl.move(speed, turn)
    threading.Timer(0.01,task).start()
	
def on_press(key):
    global up,down,left, right
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:        
        if key==keyboard.Key.up:
            up=True;
        elif key==keyboard.Key.down:
            down=True;
        elif key==keyboard.Key.left:
            left=True;
        elif key==keyboard.Key.right:
            right=True;
        #print('special key {0} pressed'.format(key))
        #print('up:{0} down:{1} left:{2} right:{3}'.format(up, down, left, right))
			
def on_release(key):
    global up,down,left, right
    if key == keyboard.Key.esc:        
        return False
    if key==keyboard.Key.up:
        up=False;
    elif key==keyboard.Key.down:
        down=False;
    elif key==keyboard.Key.left:
        left=False;
    elif key==keyboard.Key.right:
        right=False;
    #print('{0} released'.format(key))
    #print('up:{0} down:{1} left:{2} right:{3}'.format(up, down, left, right))


if __name__ == '__main__':
    logging.basicConfig(filename='sumo.log', level=logging.INFO)
    main()
