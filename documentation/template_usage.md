#

## Requirements
- Gradle (tested with 4.4.1)
- Java (tested with openjdk 11.0.16)
- MicroSD or microSDHC card, larger than 2GB. Max size 32GB. (microSDXC will not work. )
- Computer with an adapter for the SD card
- Internet connection to the brick - we used a wifi dongle

## Setup

### General
- EV3Dev https://www.ev3dev.org/ - tests have been only done with ev3dev-stretch

### ev3dev installation

1. Download ev3dev image https://www.ev3dev.org/ 
2. Flash it to the card. Ev3dev site suggests using https://www.balena.io/etcher/, it worked for us.
3. We suggest using electric tape or such to attach an impromptu handle to the SD card. Otherwise removing it from the brick might require pliers.

### Gradle project usage
- Template project source https://github.com/ev3dev-lang-java/template-project-gradle
- Set correct IP in /logomotion_gradle/config.gradle - once your brick has connection to internet, the IP should be at the top of the screen of your brick.
    - This should be enough, but if you encounter problems check main class from manifest.
- Wheel distance & wheel size ought to be set in logomotion/logomotion_gradle/src/main/java/logo line 9
<code>EV3MovePilot robot = new EV3MovePilot(wheel_size, wheel_distance);</code>
- The project supplies gradle commands you can either
    - write gradle tasks, which should list them in the terminal
    - Find them listed in logotmotion/logomotion_gradle/gradle/deploy.gradle
    - Use gradle deployAndRun