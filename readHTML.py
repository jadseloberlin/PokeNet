import glob
import os
import math
import pokemon
import player;

def main():
    path = 'C:\Users\toon1\Documents\GitHub\PokeNet/*.html' #note C:
    files = glob.glob(path)
    for name in files:
        try:
            with open(name) as f:
                for line in f:
                    firstString = line[0]
                    firstChar = firstString[0]
                    if firstChar == "|":
                        

        except IOError as exc: #Not sure what error this is
            if exc.errno != errno.EISDIR:
                raise

if __name__=="__main__":
main()
