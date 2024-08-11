public class Camarote extends IngressoVip{
    protected double valorCamarote;

    public Camarote(double valorIngresso, double valorAdicional, double valorCamarote){
        super(valorIngresso, valorAdicional);
        this.valorCamarote = valorCamarote;
    }

    public double getValorCamarote(){
        return this.valorCamarote + getValorIngressoVip();
    }
}