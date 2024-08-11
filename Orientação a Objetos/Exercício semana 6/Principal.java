public class Principal{
    public static void main(String[] args){
        Imovel[] imoveis = new Imovel[200];

        for(int i = 0; i < imoveis.length; i++){
            Endereco endereco = new Endereco("Rua " + i, "Bairro " + i, "Cidade " + i, "Estado " + i, i);
            double preco = 2 * i;
            if(i%2==0){
                imoveis[i] = new ImovelNovo(endereco, preco);
            }
            else{
                imoveis[i] = new ImovelVelho(endereco,preco);
            }
        }

        for(Imovel imovel : imoveis){
            System.out.println("Valor: " + imovel.calcularValorImovel());
        }
    }
}

// usado polimorfismo de inclusao(superclasses),