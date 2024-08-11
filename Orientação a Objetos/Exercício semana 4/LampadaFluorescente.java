public class LampadaFluorescente extends Lampada{
    private int comprimentoLampada;

    public LampadaFluorescente(boolean ligado, int comprimentoLampada){
        super(ligado);
        this.comprimentoLampada = comprimentoLampada;
    }

    public int getComprimentoLampada(){
        return this.comprimentoLampada;
    }

    public void setComprimentoLampada(int comprimentoLampada){
        this.comprimentoLampada = comprimentoLampada;
    }
}