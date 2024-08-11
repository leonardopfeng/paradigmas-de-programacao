import java.util.ArrayList;
import java.util.List;

public class CorridaDeObstaculo implements Corrida{
    private List<String> participantes = new ArrayList<>();

    public void inscreverParticipante(String nome){
        participantes.add(nome);
        System.out.println("Participante " + nome + " inscrito na corrida de obstaculo");
    }

    public void entregarKit(String nome){
        if(participantes.contains(nome)){
            System.out.println("Participante " + nome + " recebeu o kit");
        }
        else{
            System.out.println("Participante não inscrito na corrida");
        }
    }
}