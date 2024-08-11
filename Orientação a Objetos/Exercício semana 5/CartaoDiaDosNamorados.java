public class CartaoDiaDosNamorados extends CartaoWeb{

    public CartaoDiaDosNamorados(String destinatario){
        super(destinatario);
    }

    public String retornarMensagem(String remetente){
        return "Dia dos namorados" + remetente;
    }
}