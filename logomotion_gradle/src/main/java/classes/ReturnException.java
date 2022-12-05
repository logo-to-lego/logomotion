package classes;

public class ReturnException extends Exception {
    private Variable returnValue;

    public ReturnException(Variable variable) {
        this.returnValue = variable;
    }

}
