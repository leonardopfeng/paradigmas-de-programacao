public class PrincipalIngresso{
    public static void main(String[] args){
        Ingresso ingresso = new Ingresso(100);
        IngressoVip ingressoVip = new IngressoVip(200, 30);
        Camarote camarote = new Camarote(150, 20, 30);

        System.out.println(ingresso.getValorIngresso());
        System.out.println(ingressoVip.getValorIngresso());
        System.out.println(ingressoVip.getValorIngressoVip());
        System.out.println(camarote.getValorIngresso());
        System.out.println(camarote.getValorIngressoVip());
        System.out.println(camarote.getValorCamarote());
    }
}