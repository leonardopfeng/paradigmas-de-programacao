public class PrincipalContador{
    public static void main(String[] args){
        Contador contador = new Contador(10);
        contador.zeroCounter();
        System.out.println(contador.counter);
    }
}