package example;

import ev3dev.actuators.lego.motors.EV3LargeRegulatedMotor;
import ev3dev.sensors.Battery;
import ev3dev.robotics.tts.Espeak;
import lejos.hardware.port.MotorPort;
import lejos.utility.Delay;

public class MyFirstRobot {

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
		TTS.setVolume(100);
		TTS.setSpeedReading(200);
		TTS.setPitch(150);
		TTS.setVoice("fi");
		TTS.setMessage("Miksi pitaa kayttaa javaa?");
		TTS.say();
		Delay.msDelay(3000);
        
        System.out.println("Defining the Stop mode");
        motorLeft.brake();
        motorRight.brake();

        System.out.println("Defining motor speed");
        final int motorSpeed = 500;
        motorLeft.setSpeed(motorSpeed);
        motorRight.setSpeed(motorSpeed);

        System.out.println("Go Forward with the motors");
        motorLeft.forward();
        motorRight.forward();

        Delay.msDelay(2000);

        System.out.println("Stop motors");
        motorLeft.stop();
        motorRight.stop();

        System.out.println("Go Backward with the motors");
        motorLeft.backward();
        motorRight.backward();

        Delay.msDelay(2000);

        System.out.println("Stop motors");
        motorLeft.stop();
        motorRight.stop();

        System.out.println("Checking Battery");
        System.out.println("Votage: " + Battery.getInstance().getVoltage());
        
        TTS.setMessage("Olen hyva java poika.");
        TTS.say();

        System.exit(0);
    }
}
