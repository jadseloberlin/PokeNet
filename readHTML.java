import java.io.*;
import java.util.*;
import player;
import pokemon;

public class ReadHTML{
  Player p1;
  Player p2;


  public static void main(String[] args){
    String path = 'C:\Users\toon1\Documents\GitHub\PokeNet/*.html';
    File dir = new File(path);
    File[] files = dir.listFiles();
    for (File f : files){
      if(f.isFile()){
        BufferedReader inputStream = null;
        try{
          inputStream = newBufferedReader(new FileReader(f));
          String line;
          while((line=inputStream.readLine()) != null){
            String firstString = line[0];
            char firstChar = firstString[0];
            if (firstChar == '|'){
              List<String> info = Arrays.asList(line.split('|'));
              String firstWord = info[0];


            }//if
          }//while
        }//try

      }//end if
    }//for
  }//main

  public static Player playerProcess(List<String> playerInfo){

  }



}
