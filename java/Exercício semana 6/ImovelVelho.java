public class ImovelVelho extends Imovel{
    public ImovelVelho(Endereco endereco, double preco){
        super(endereco, preco);
    }

    public double calcularValorImovel(){
        return this.preco * 0.8;
    }
}