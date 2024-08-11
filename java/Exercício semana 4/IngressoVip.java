public class IngressoVip extends Ingresso{
    protected double valorAdicional;

    public IngressoVip(double valorIngresso, double valorAdicional){
        super(valorIngresso);
        this.valorAdicional = valorAdicional;
    }

    public double getValorIngressoVip(){
        return this.valorAdicional + getValorIngresso();
    }
}