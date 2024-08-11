import java.util.ArrayList;
import java.util.List;

public class Principal{
    public static void main(String[] args){
        List<Corrida> corridas = new ArrayList<>();
        corridas.add(new CorridaDeRua());
        corridas.add(new CorridaDeObstaculo());

        Gerenciar gerenciarCorrida = new Gerenciar();

        for(Corrida corrida : corridas){
            gerenciarCorrida.inscrever(corrida, "Joao");
            gerenciarCorrida.entregar(corrida, "Joao");
        }
    }
}