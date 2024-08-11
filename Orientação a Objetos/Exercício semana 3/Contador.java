public class Contador{
    protected int counter;

    public Contador(int counter){
        this.counter = counter;
    }

    public int getCounter(){
        return this.counter;
    }

    public void setCounter(int counter){
        this.counter = counter;
    }

    public void zeroCounter(){
        this.counter = 0;
    }

    public void increaseCounter(){
        this.counter = this.counter + 1;
    }

    public void decreaseCounter(){
        if(this.counter > 0){
            this.counter = this.counter - 1;
        }
    }
}