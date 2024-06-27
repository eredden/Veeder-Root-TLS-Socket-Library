import unittest
from tls_3xx_functions import split_data

# Verify that split_data() correctly splits apart chunks of data.
class test_split_data(unittest.TestCase):
    def test_split_data(self):
        data = ["abcdefabcdef", 
                "zyxwzyxw", 
                "ABCabcABC",
                "ABCabcABC"]
        
        length = [3,
                  4,
                  3,
                  10]
        
        expected = [["abc", "def", "abc", "def"], 
                    ["zyxw", "zyxw"], 
                    ["ABC", "abc", "ABC"],
                    ["ABCabcABC"]]

        for index in range(0, len(data)):
            actual = split_data(data[index], length[index])
            self.assertEqual(actual, expected[index])

if __name__ == "__main__":
    unittest.main()