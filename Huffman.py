import os
import heapq
from bitarray import bitarray
  
# A Huffman Tree Node 
class node: 
    def __init__(self, freq, symbol, left=None, right=None): 
        # frequency of symbol 
        self.freq = freq 
  
        # symbol name (character) 
        self.symbol = symbol 
  
        # node left of current node 
        self.left = left 
  
        # node right of current node 
        self.right = right 
  
        # tree direction (0/1) 
        self.huff = '' 
  
    # less than operator
    def __lt__(self, nxt): 
        return self.freq < nxt.freq 
  

class Huffman:
    def __init__(self, filename):
        self.filename = filename
        self.encoding = {}
        self.frequency = {}
        self.root = None
        self.decoded_bit_length = 0

    def printTable(self):
        self.getEncoding(self.root)
        message = f"\nFilename: {self.filename}\n"
        for key in self.encoding:
            message += f"{key}: encoding -> {self.encoding[key]} | freq -> {self.frequency[key]}\n"
        print(message)

    def getEncoding(self, node, val=''):
        newVal = val + str(node.huff) 
    
        if(node.left): 
            self.getEncoding(node.left, newVal) 
        if(node.right): 
            self.getEncoding(node.right, newVal) 
    
        if(not node.left and not node.right): 
            self.encoding[node.symbol] = newVal

    def encode(self):
        """
        Takes a .txt file and encodes it to a separate binary file using huffman encoding
        returns the huffman table created to encode data
        """
        if not self.filename.lower().endswith('.txt'):
            raise Exception("File must be a .txt file")
        
        with open('texts/' + self.filename, 'r', encoding="utf8") as file:
            data = file.read()

            self.frequency = {}
            for char in data:
                if char in self.frequency:
                    self.frequency[char] += 1
                else:
                    self.frequency[char] = 1
            
            # min heap of huffman nodes, smallest frequency first
            nodes = []
            for key in self.frequency:
                heapq.heappush(nodes, node(freq=self.frequency[key], symbol=key))

            while len(nodes) > 1: 

                left = heapq.heappop(nodes)
                right = heapq.heappop(nodes) 
            
                left.huff = 0
                right.huff = 1
            
                newNode = node(left.freq+right.freq, left.symbol+right.symbol, left, right) 
                heapq.heappush(nodes, newNode) 

            self.root = nodes[0]
            self.getEncoding(self.root)
            
            bit_string = ""
            for char in data:
                bit_string += self.encoding[char]
            self.decoded_bit_length = len(bit_string)

            while len(bit_string) % 8 != 0:
                bit_string += "0"

            def _to_Bytes(data):
                b = bytearray()
                for i in range(0, len(data), 8):
                    b.append(int(data[i:i+8], 2))
                return bytes(b)

            outfile = 'bin/' + self.filename[:-4] + '.bin'
            with open(outfile, 'wb') as file:
                file.write(_to_Bytes(bit_string))


            original = os.path.getsize('texts/' + self.filename)
            compressed = os.path.getsize('bin/' + self.filename[:-4] + '.bin')
            print(f"\nEncoding complete. File saved as {outfile}")
            print(f'Original file: {original} bytes')
            print(f'Compressed file: {compressed} bytes')
            print(f'Compression ratio: {round((original/compressed), 2)}x')
            print(f'Compressed file to about {round(((compressed)/original)*100)}% of original')

    def decode(self):
        with open('bin/' + self.filename[:-4] + '.bin', 'rb') as file:
            arr = file.read()
            bit_stream = ''.join(format(byte, '08b') for byte in arr)

            ans = ""
            curr = self.root
            for i in range(self.decoded_bit_length):
                if bit_stream[i] == "0":
                    curr = curr.left
                else:
                    curr = curr.right
        
                # reached leaf node
                if curr.left is None and curr.right is None:
                    ans += curr.symbol
                    curr = self.root
            
            # write to text file
            with open('decoded/' + self.filename, 'w', encoding="utf8") as file:
                file.write(ans)

            print(f"\nDecoding complete. File saved in decoded/{self.filename[:-4]}_decoded.txt")

