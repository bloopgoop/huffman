from Huffman import Huffman
import unittest

class TestHuffman(unittest.TestCase):
    def test_encode_works(self):
        """ Check that when encoding a file, the huffman table is created """
        filename = "encode_test.txt"
        with open('texts/' + filename, 'w', encoding="utf8") as file:
            file.write("Hello World")
        huff = Huffman(filename)
        huff.encode()
        self.assertTrue(len(huff.encoding) > 0)

    def test_bin_correctness(self):
        """ Check if the binary file is correct """
        filename = "encode_test.txt"
        with open('texts/' + filename, 'w', encoding="utf8") as file:
            file.write("Hello World")
        huff = Huffman(filename)
        huff.encode()
        
        with open('bin/' + filename[:-4] + '.bin', 'rb') as file:
            data = file.read()
            self.assertEqual(data, b'\x5F\x58\x3D\xD1')

    def test_decode_works(self):
        """ Check that when decoding a binary file, the original text is recovered """
        filename = "decode_test.txt"
        texts = [
            "Hello World", 
            "Apples are great", 
            "I like trains", 
            "I like turtles",
            "The quick brown fox jumps over the lazy dog",
            "The five boxing wizards jump quickly",
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
            ]
        
        test_passed = True
        for text in texts:
            with open('texts/' + filename, 'w', encoding="utf8") as file:
                file.write(text)

            huff = Huffman(filename)
            huff.encode()
            huff.decode()
            with open('decoded/' + filename, 'r', encoding="utf8") as file:
                data = file.read()
                test_passed = test_passed and (data == text)
        
        self.assertTrue(test_passed)


if __name__ == '__main__':
    unittest.main()