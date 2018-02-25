# Sumo Control

Tried to improve control of the excellent work of [frankibem/sumo-control](https://github.com/frankibem/sumo-control)
Main change is using pynput in place of opencv::waitkey
I plan to implement Postures in few time...

## Requirements
More requirements will be added as the project progresses.

### Software
- Python 3
- OpenCV
- pyinput

### Hardware
- One Jumping Sumo 
- Several batteries

## Miscellaneous
- The minidrone module was adapted from [forthtemple/py-faster-rcnn](https://github.com/forthtemple/py-faster-rcnn) and [haraisao/JumpingSumo-Python
](https://github.com/haraisao/JumpingSumo-Python). As I am only interested in ground motion, I have limited my implementation to that (no jumping, ...)
- The Parrot ARSDK3 document can be found [here](http://developer.parrot.com/docs/bebop/ARSDK_Protocols.pdf). I was also able to find some useful information on their [GitHub](https://github.com/Parrot-Developers) page.
