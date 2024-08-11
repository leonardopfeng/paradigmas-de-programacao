public class Telefone{
    protected int ddi;
    protected int ddd;
    protected int numero;

    public Telefone(int ddi, int ddd, int numero){
        setDdi(ddi);
        this.ddd = ddd;
        this.numero = numero;
    }

    public int getDdi(){
        return this.ddi;
    }

    public void setDdi(int ddi){
        if((ddi == 55) || (ddi == 61)){
            this.ddi = ddi;
        }
    }

    public void cadastrar(int ddi, int ddd, int numero){
        setDdi(ddi);
        this.ddd = ddd;
        this.numero = numero;
    }

    public String exibir(){
        return "+" + this.ddi + " " + this.ddd + " " + this.numero;
    }
}
