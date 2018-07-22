import java.util.Map;
import java.lang.Character;
import java.util.HashMap;


class Reverse{
public static void main(String args[]){
    String input = args[0];
    int inputNum = Integer.parseInt(args[0], 10);
    String baseTenNormal = "x (base 10): " + args[0];
    String base16Normal = "x (base 16): " + Integer.toString(inputNum, 16);

    System.out.println(baseTenNormal);
    System.out.println(base16Normal);

}

}
