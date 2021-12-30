## LIT
LIT: A lightweight approach to generalize playtesting tactics from manual testing, and to adopt the tactics for automatic game testing.

This is a research prototype of  the LIT approach for automatic game testing.

## Structure
![structure](https://user-images.githubusercontent.com/92325589/147783626-74d2467d-99ee-4583-affd-e74e9c5615fc.png)

• BIN
	• RECORDER.PY     : record the user traces 
	• ANALYZER.PY     : analyze the user traces, action type analysis
	• MODUEL_GEN.PY   : pattern inferrence
	• TESTCASE_GEN.PY : load the module to generate test cases 
	• TEST.PY         : test games
• CONF
	• CONFIG.INI : configuration for the system and games.
• LIBS
	• ADBLIBS : all functions related with adb tool  
	• SCREENLIBS : all functions related with screen image. Like matching image, getting image resolution and so on .
• DATA
	• TRACES : generated playing traces by recorder.py
	• ACTIONS: 
	• MODULES:
	
• LOG
• IMAGE
	• FUNCTION IMAGE 
	• PLAY IMAGE
![image](https://user-images.githubusercontent.com/92325589/147786246-a6ef6c8e-1b41-431f-b1e6-14805ab13e67.png)


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




