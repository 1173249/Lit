## LIT
LIT: A lightweight approach to generalize playtesting tactics from manual testing, and to adopt the tactics for automatic game testing.

This is a research prototype of  the LIT approach for automatic game testing.

## Structure
![structure](https://user-images.githubusercontent.com/92325589/147783626-74d2467d-99ee-4583-affd-e74e9c5615fc.png)

![image](https://user-images.githubusercontent.com/92325589/147786479-dd0ccc65-6194-4aef-ba2f-84c6f617354b.png)



## Installation
Simply clone the source code from this repository and apply the follwing enviroment configuration


## Enviroment Configration
* PYTHON >= 3.6.9
* ANDROID SDK >= 6.0
* Ubuntu 
* EMULATOR OR DEVICES
* ADB
* OpenCV
* Configparser
* Numpy
* Scipy
* codecs


## USAGE
### conf 
edit the config.ini, specify SDK PATH, device name AND mobile games you want to test.
there are already 9 games built in tools as seen in the config file.

### image
upload function icon , play icon and target icons if needed into the image folder.

There are two ways to run the tool
* 1. step by step
python recorder.py : following the instruction to play the game as a real user, kill the script if you think the training is long enough
python analyzer.py
python module_gen.py
python testcase_gen.py
python play.py

* 2.tooltest script
bash -x tooltest.sh run the test automatically

## OUTPUT 
* coverage - coverage files are stored here
* crash -- Crash reports

## Experiment
The experiments are conducted at Emulator and Google Pixel XL 
![image](https://user-images.githubusercontent.com/92325589/147787729-d671026d-838f-43d5-bb7a-f24f598af485.png)




