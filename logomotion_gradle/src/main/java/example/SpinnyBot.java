package example;

import ev3dev.actuators.lego.motors.EV3LargeRegulatedMotor;
import ev3dev.robotics.tts.Espeak;
import lejos.hardware.port.MotorPort;
import lejos.utility.Delay;

public class SpinnyBot {

    public static void main(final String[] args){

        System.out.println("Creating Motor C & B");
        final EV3LargeRegulatedMotor motorLeft = new EV3LargeRegulatedMotor(MotorPort.C);
        final EV3LargeRegulatedMotor motorRight = new EV3LargeRegulatedMotor(MotorPort.B);

        //To Stop the motor in case of pkill java for example
        Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {
            public void run() {
                System.out.println("Emergency Stop");
                motorLeft.stop();
                motorRight.stop();
            }
        }));
        
        Espeak TTS = new Espeak();
		TTS.setVolume(200);
		TTS.setSpeedReading(100);
		TTS.setPitch(100);
		TTS.setVoice("fi");
		TTS.setMessage("viiiiiiiiiiiii");
        
        System.out.println("Defining the Stop mode");
        motorLeft.brake();
        motorRight.brake();

        System.out.println("Defining motor speed");
        int motorSpeed = 10;
        motorLeft.setSpeed(motorSpeed);
        motorRight.setSpeed(motorSpeed);

        System.out.println("Start spinning.");
        motorLeft.forward();
        motorRight.backward();
        for(int i = 0; i<50; i++) {
            Delay.msDelay(250);
            motorLeft.setSpeed(motorSpeed);
            motorRight.setSpeed(motorSpeed);
            motorLeft.forward();
            motorRight.backward();
            if (i%10 == 0) {
                System.out.println("Saying whee!");
                TTS.say();
            }
            motorSpeed += 10;
        }

        System.out.println("Stop motors");
        motorLeft.stop();
        motorRight.stop();

        System.out.println("Saying whee!");
        TTS.say();
        Delay.msDelay(1000);
        System.out.println("Speeding off");
        motorLeft.setSpeed(1000);
        motorRight.setSpeed(1000);
        motorLeft.forward();
        motorRight.forward();
        Delay.msDelay(500);
        motorLeft.stop();
        motorRight.stop();

        System.exit(0);
    }
}
