public class Lampada{
    protected boolean ligado;

    public Lampada(boolean ligado){
        this.ligado = ligado;
    }

    public boolean isLigado(){
        return this.ligado;
    }

    public void setLigado(boolean ligado){
        this.ligado = ligado;
    }
}