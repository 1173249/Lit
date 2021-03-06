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


## Usage
### conf 
edit the config.ini, specify SDK PATH, device name AND mobile games you want to test.
there are already 9 games built in tools as seen in the config file.

### image
upload function icon , play icon and target icons if needed into the image folder.

There are two ways to run the tool
### step by step

![image](https://user-images.githubusercontent.com/92325589/147788578-736db8d6-9da0-4339-b4c6-1b27729faa01.png)


### tooltest script
bash -x tooltest.sh run the test automatically

## Output 
* coverage - coverage files are stored here

## Experiment
The experiments were conducted at Emulator for open-source games and Google Pixel XL for close-source games.
![image](https://user-images.githubusercontent.com/92325589/147787729-d671026d-838f-43d5-bb7a-f24f598af485.png)

we use code coverage to evaluate the performance. And include game score and game level.  
Given a game G, the first author manually played G for eight minutes in LIT ’s demo mode, and then switched to
LIT’s test mode to automatically play G for one hour.

![image](https://user-images.githubusercontent.com/92325589/147788991-7de18a55-a8d9-437a-a41f-d444fa214155.png)

Based on eight-minute user demos,LIT effectively earned game scores, passed difficulty levels, and executed lots of code within one-hour playtest.

![image](https://user-images.githubusercontent.com/92325589/147789023-86b13170-ab23-47d6-8505-f61998c7c03c.png)

LIT outperformed Monkey and Sapienz by  always  acquiring  higher  scores  and  passing  more  levels.
RLT  worked  worse  than  LIT in  most  scenarios with same training time. 



