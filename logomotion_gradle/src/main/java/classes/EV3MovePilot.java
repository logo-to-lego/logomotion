package classes;

import ev3dev.actuators.lego.motors.EV3LargeRegulatedMotor;
import lejos.hardware.port.MotorPort;
import lejos.utility.Delay;
import java.lang.Math;

public class EV3MovePilot {
    double wheelDiameter;
    double wheelDistance;
    double wheelCircumference;
    double rotationCircumference;
    int motorSpeed;
    int motorRotationSpeed;
    EV3LargeRegulatedMotor leftMotor;
    EV3LargeRegulatedMotor rightMotor;

    public EV3MovePilot() {
        // Start params
		this.wheelDiameter = 5.6;
		this.wheelDistance = 11.7;
        this.wheelCircumference = Math.PI*this.wheelDiameter;
        this.rotationCircumference = Math.PI*wheelDistance;
		this.motorSpeed = 500;
		this.motorRotationSpeed = 250;
		this.leftMotor = new EV3LargeRegulatedMotor(MotorPort.A);
		this.rightMotor = new EV3LargeRegulatedMotor(MotorPort.B);
        this.leftMotor.brake();
        this.rightMotor.brake();
        // End params
    }

    public void setSpeed(int speed) {
        this.motorSpeed = speed;
    }

    public void travel(double distance) {
        this.leftMotor.setSpeed(this.motorSpeed);
        this.rightMotor.setSpeed(this.motorSpeed);
        double fullRotations = Math.abs(distance)/this.wheelCircumference;
        double fullRotationTime = 360.0/this.motorSpeed;
        double travelTime = fullRotations * fullRotationTime;
        if(distance > 0) {
            this.rightMotor.forward();
            this.leftMotor.forward();
        } else {
            this.rightMotor.backward();
            this.leftMotor.backward();
        }
        Delay.msDelay((long) (travelTime*1000));
        this.rightMotor.stop();
        this.leftMotor.stop();
    }

    public void rotate(double angle) {
        this.leftMotor.setSpeed(this.motorRotationSpeed);
        this.rightMotor.setSpeed(this.motorRotationSpeed);
        double distance = angle*(Math.PI/180)*(this.wheelDistance/2);
        double fullRotations = Math.abs(distance)/this.wheelCircumference;
        double fullRotationTime = 360.0/this.motorRotationSpeed;
        double travelTime = fullRotations * fullRotationTime;
        if(angle > 0) {
            this.leftMotor.backward();
            this.rightMotor.forward();
        } else {
            this.leftMotor.forward();
            this.rightMotor.backward();
        }
        Delay.msDelay((long) (travelTime*1000));
        this.rightMotor.stop();
        this.leftMotor.stop();
    }
}
