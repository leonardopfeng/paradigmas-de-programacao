public class Gerenciar{
    public void inscrever(Corrida corrida, String nome){
        corrida.inscreverParticipante(nome);
    }

    public void entregar(Corrida corrida, String nome){
        corrida.entregarKit(nome);
    }
}