public class PrincipalTelefone{
    public static void main(String[] args){
        Telefone[] telefones = new Telefone[2];
        telefones[0] = new Telefone(55, 42, 9999999);
        telefones[1] = new Telefone(10, 43, 9999999);

        for(Telefone telefone : telefones){
            System.out.println(telefone.exibir());
        }
    }
}