## LIT
LIT: A lightweight approach to generalize playtesting tactics from manual testing, and to adopt the tactics for automatic game testing.

This is a research prototype of  the LIT approach for automatic game testing.

## Structure
![structure](https://user-images.githubusercontent.com/92325589/147783626-74d2467d-99ee-4583-affd-e74e9c5615fc.png)

![image](https://user-images.githubusercontent.com/92325589/147786479-dd0ccc65-6194-4aef-ba2f-84c6f617354b.png)



## Installation
Simply clone the source code from this repository and apply the follwing enviroment configuration


## Enviroment Configration
* PYTHON
* ANDROID SDK
* LINUX
* EMULATOR OR DEVICES

##USAGE
* conf 
edit the config.ini, specify SDK PATH, AND testing object you want to test
* image
upload function icon , play icon and target icons if need into the image folder
* bin

python recorder.py : following the instruction to play the game as a real user, kill the script if you think the training is long enough
python analyzer.py
python module_gen.py
python testcase_gen.py
python play.py

* script
bash -x tooltest.sh run the test automatically

## OUTPUT 
* coverage - coverage files are stored here
* crash -- Crash reports




