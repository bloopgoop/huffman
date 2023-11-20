"""
HOW TO RUN:

create a txt file in the texts folder, write some text in it
run runner.py
enter the name of the file you created eg "test.txt"

"""
from Huffman import Huffman

def main():
    filename = input("Enter the name of the file to encode: ")
    huff = Huffman(filename)
    huff.encode()
    #huff.printTable()
    huff.decode()

if __name__ == "__main__":
    main()