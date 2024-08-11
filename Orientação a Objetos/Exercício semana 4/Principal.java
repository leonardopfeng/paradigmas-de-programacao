public class Principal{
    public static void main(String[] args){
        LampadaFluorescente lampadaF = new LampadaFluorescente(true, 10);
        System.out.println(lampadaF.getComprimentoLampada());
        System.out.println(lampadaF.isLigado());        
        lampadaF.setLigado(false);
        lampadaF.setComprimentoLampada(1000);
        System.out.println(lampadaF.getComprimentoLampada());
        System.out.println(lampadaF.isLigado()); 
    }
}