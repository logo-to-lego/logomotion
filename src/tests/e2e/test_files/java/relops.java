package logo;

import classes.EV3MovePilot;
import java.lang.Runnable;

public class Logo {

    public static void main(String[] args) {
        EV3MovePilot robot = new EV3MovePilot();
        Logo logo = new Logo();
        
        double temp1 = 5.123;
        var var2 = temp1;
        double temp3 = 20.6;
        double temp4 = -temp3;
        var var5 = temp4;

        boolean temp6 = var2 < var5;
        var var7 = temp6;
        boolean temp8 = var2 <= var5;
        var var9 = temp8;
        boolean temp10 = var2 > var5;
        var var11 = temp10;
        boolean temp12 = var2 >= var5;
        var var13 = temp12;
        boolean temp14 = var2 == var5;
        var var15 = temp14;
        boolean temp16 = var2 != var5;
        var var17 = temp16;

        String temp18 = "kissa";
        var var19 = temp18;
        String temp20 = "vesinokkaeläin";
        var var21 = temp20;
        
        boolean temp22 = var19 == var21;
        var var23 = temp22;
        boolean temp24 = var19 != var21;
        var var25 = temp24;
    }
}