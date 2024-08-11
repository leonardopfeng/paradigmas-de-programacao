public class CartaoNatal extends CartaoWeb{

    public CartaoNatal(String destinatario){
        super(destinatario);
    }

    public String retornarMensagem(String remetente){
        return "Natal" + remetente;
    };
}