public abstract class Imovel{
    protected Endereco endereco;
    protected double preco;

    public Imovel(Endereco endereco, double preco){
        this.endereco = endereco;
        this.preco = preco;
    }

    public abstract double calcularValorImovel();
}