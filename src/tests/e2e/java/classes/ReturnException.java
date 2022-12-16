package classes;

public class ReturnException extends Exception {
    public Variable returnValue;

    public ReturnException(Variable variable) {
        this.returnValue = variable;
    }

}
