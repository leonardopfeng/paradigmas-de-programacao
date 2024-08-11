public class ImovelNovo extends Imovel{
    public ImovelNovo(Endereco endereco, double preco){
        super(endereco, preco);
    }

    public double calcularValorImovel(){
        return this.preco * 1.2;
    }
}