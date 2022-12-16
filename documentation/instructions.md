# Instructions

This manual contains step-by-step instructions on how to
* download the required tools to compile from logo to java
* setup EV3 robot
* transfer java to the robot

Also this file contains instructions on how to write your own code generator

Before going further, you need to have:
* Python3. We are using version 3.7.2 and greater
* Git
* LEGO MINDSTORMS EV3 Intelligent Brick
* MicroSD or microSDHC card, larger than 2GB but max size 32GB (microSDXC will not work)
* Computer that can read and write to an SD card
* Internet connection to the EV3 brick - we used a wifi dongle

**Disclaimer:** This manual was tested with macOS Ventura 13.0.1. Linux has been working for us as well, but Windows has caused problems.

## Getting the tools

Clone this repo by running `git clone git@github.com:logo-to-lego/logomotion.git`.

### Poetry
1. [Poetry](https://pypi.org/project/poetry/) makes it easier to handle dependencies and run the program with coherent commands. Install poetry with `pip3 install poetry`.
2. After installing poetry, go to the logomotion directory, and run `poetry install`.
3. The setup with poetry should now be done. List invoke commands with `poetry run invoke --list`. E.g. you can try to run tests with `poetry run invoke test`.

### Java and Gradle

Gradle is required to be installed. We have used different Gradle versions with each computer we have tested, but it different gradle versions might require different versions of Java.

Install gradle. Check out instructions from [gradle](https://gradle.org/install/).

You are going to need Java for compiling. The [build.gradle](https://github.com/logo-to-lego/logomotion/blob/main/logomotion_gradle/build.gradle) uses Java 11 which can be downloaded from [here](https://www.oracle.com/java/technologies/downloads/). Oracle requires you to have account to install java.

Atleast with MacOS users multiple java versions can be installed. Check out this [link](https://medium.com/reachnow-tech/change-default-java-version-on-mac-a7f01647f126) on how to change the default java version on your computer.

### EV3

#### Flash EV3dev image
Download EV3dev image from [ev3dev](https://www.ev3dev.org/docs/getting-started/). Connect the MicroSD or microSDHC card to your computer and flash the image to the card. [ev3dev](https://www.ev3dev.org/docs/getting-started/) suggests using [Etcher](https://www.balena.io/etcher/). It worked for us.

#### Connecting to the EV3 Brick via wifi dongle
The brick must be in connected to the same wifi as your computer. We have used hotspots from our phones. 

Once your brick has connection to internet, the IP should be at the top of the screen of your brick. Set the IP-address of the brick in **/logomotion_gradle/config.gradle**

### Running the code
Run the logo code with `poetry run invoke start path_to_your_logo_code.logo` so for example `poetry run invoke start logo/move.logo`. If there are no errors, java code is generated to logomotion_gradle/src/main/java/logo/Logo.java. If there were errors, java is not generated. 

Change your directory to logomotion_gradle with `cd logomotion_gradle` and run `./gradlew deployAndRun`. 

That should be all there is. After about a minute the robot should be doing what the given logo code defined.

### Problems and checks

We had some problems with gradle. For some reason, the gradle project did not connect to the robot and threw a timeout error after about 100 seconds. The solution was caused by incompatible java version and gradle wrapper version. The solution was to update gradle wrapper, which was done from Visual Studio Code.

VPN can also cause problems with connecting to the robot. So turn off VPN.

Check also that you have the correct motor ports configured in [.env](https://github.com/logo-to-lego/logomotion/blob/user-manual/.env)

## Create your own code generator

If you wish to compile logo to some other language than java, like python, you need to build a new CodeGenerator class. The default java code generator is in [src/code_generator](https://github.com/logo-to-lego/logomotion/blob/main/src/utils/code_generator.py). Implement the classes methods to your code generator class. Working with Java has required us to do some tricks here and there, so all the method names might not be logical with your language.

In [main.py](https://github.com/logo-to-lego/logomotion/tree/main/src/code_generator) add your language settings in method [get_code_generator](https://github.com/logo-to-lego/logomotion/blob/main/src/main.py#L18). The [CODE_GEN_LANG](https://github.com/logo-to-lego/logomotion/blob/main/src/main.py#L100) is defined in the [.env](https://github.com/logo-to-lego/logomotion/blob/main/.env) file.

For testing purposes we transfered python code to the EV3 Brick with SSH. There might be more automated tools to do the job.

