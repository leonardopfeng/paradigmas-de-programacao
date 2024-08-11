public class Principal{

    public static void main(String[] args){
        
        CartaoWeb[] cartoes = new CartaoWeb[3];
        cartoes[0] = new CartaoDiaDosNamorados("DDN");
        cartoes[1] = new CartaoAniversario("Aniversario");
        cartoes[2] = new CartaoNatal("Natal");

        for(CartaoWeb cartao : cartoes){
            System.out.println(cartao.retornarMensagem("Cartao"));
        }
    }
}
