# dictionary.py — ScrabbleDict: loads and validates 5-letter words
# Author: Priyanshu Pusola


class ScrabbleDict:

    def __init__(self, size, filename):
        '''
        Loads all words of the given length from filename into a dictionary
        keyed by word, valued by first letter.
        '''
        self.dictionary = {}
        self.size = size
        self.filename = filename
        with open(filename, 'r') as file:
            for line in file:
                word = line.strip()
                if len(word) == self.size:
                    self.dictionary[word] = word[0]  # value is first letter

    def check(self, word):
        '''Returns True if word is in the dictionary.'''
        return word in self.dictionary

    def getSize(self):
        '''Returns the total number of words in the dictionary.'''
        return len(self.dictionary)

    def getWords(self, letter):
        '''Returns a sorted list of all words starting with the given letter.'''
        return sorted(w for w in self.dictionary if w[0] == letter.lower())

    def getWordSize(self):
        '''Returns the fixed word length (5).'''
        return self.size


# ── Tests ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Creating ScrabbleDict with size=5 and file='scrabble5.txt'")
    dictionary = ScrabbleDict(5, 'scrabble5.txt')

    print(f"1. 'aunty'  -> True.   Got: {dictionary.check('aunty')}")
    print(f"2. 'music'  -> True.   Got: {dictionary.check('music')}")
    print(f"3. 'soccer' -> False.  Got: {dictionary.check('soccer')}")
    print(f"4. 'bazar'  -> True.   Got: {dictionary.check('bazar')}")

    print(f"Dictionary size: {dictionary.getSize()} words")

    print("Words starting with 'x':", dictionary.getWords('x'))
    print("Words starting with 't' (first 10):", dictionary.getWords('t')[:10])

    print(f"Word size: {dictionary.getWordSize()} letters")
