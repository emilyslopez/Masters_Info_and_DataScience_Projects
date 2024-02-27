"""
The Cheating at Scrabble Program contains two modules: scrabble.py and wordscore.py.

This program uses data from "sowpods.txt." It contains all of the "valid Scrabble English" words from the official words list. It
also uses the predefined "scores" dictionary which has letters as keys and their Scrabble points as values.

wordscore.py contains four functions which are used to find all valid Scrabble English words using the given character tiles,
calculate the word's score and return a list of these words with their score as a tuple and the total number of possible words as 
an integer. The functions `words_scores_list`, `score_word` and `valid_words_list` are called in scrabble.py.

Functions:
`rack_characters_count`
`valid_words_list`
`score_word` 
`words_scores_list`
"""

# Dictionary with letters and their Scrabble values:
scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
         "x": 8, "z": 10}

# Read data from sowpods.txt 
with open("sowpods.txt","r") as infile:
    raw_input = infile.readlines()
    data = [datum.strip('\n') for datum in raw_input]


def rack_characters_count(rack):
    """ Given a list of characters (tiles in the Scrabble rack), returns the frequency of each tile in the string
    Args: Scrabble rack/list of character tiles as a String
    Returns: Dictionary with tiles as a String and a count of that tile as an Integer"""

    # Make all letters uppercase for easy comparison and the output format. Make key value pairs of the tile
    # character and the amount of times that tile is present in the Scrabble rack String
    rack = rack.upper()
    return {tile: rack.count(tile) for tile in rack}


def valid_words_list(rack):
    """ Takes the given Scrabble rack from `run_scrabble` and returns a list of all valid Scrabble English words
    using our tiles.
    Args: Scrabble rack/list of character tiles as a String
    Returns: A List of pairs (Lists). First item in the pair is the valid Scrabble word. Second item are the character 
            tiles used to make the word. Ex: valid Scrabble word = 'IF', character tiles used = '?F' """
    
    # Find the amount of each character tile we have in our Scrabble rack.
    characters_count= rack_characters_count(rack)

    # For each word in `data` (sowpods.txt), checks if all of the letters in the word are present in
    # the Scrabble rack. If they are, we add the word to our list of valid words. 

    # Keep track of the number of available tile characters in our rack and the characters used to
    # make the valid word (wildcards or letters from our rack) to calculate the word's score later on.
    valid_words = []
    for word in data:
        available_characters = characters_count.copy()
        characters_used = ""
        for letter in word:
            if letter in available_characters.keys() and available_characters[letter] > 0: # the letter is available in our rack
                available_characters[letter] -= 1   # we have one less of this letter in our rack
                characters_used += letter    # add the letter to the characters used
            elif letter not in available_characters.keys() or available_characters[letter] == 0: # the letter isn't in our rack, but we have wildcards
                if "?" in available_characters.keys() and available_characters["?"] > 0: # we have a '?' wildcard
                    available_characters["?"] -= 1
                    characters_used += "?"
                elif "*" in available_characters.keys() and available_characters["*"] > 0: # we have a '*' wildcard
                    available_characters["*"] -= 1
                    characters_used += "*"
                else:   # the letter is not in our rack and we don't have wildcards, so continue to the next word
                    break
        else:
            valid_words.append([word, characters_used]) # we have all the necessary characters, add the word to our valid words list
    return valid_words


def score_word(word):
    """ Uses the scores Dict to calculate the total score for a given word.
    Args: Pair of two String words (List). First item in the pair is the valid Scrabble word. Second item are the
         character tiles used to make the word. Ex: ["IF", "?F"]
    Returns: Tuple of the score for the word as an Integer and the word itself as a String"""

    # Isolate the first and second item in the word pair to calculate the word's score.
    total_score = 0
    scrabble_word = word[0]
    user_tiles_word = word[1]
    
    # For each letter in our word, get its value using the `scores` dictionary and add that value to the word's total score.
    # If the character in our word is a wildcard ('?' or '*'), it's value is 0 so we don't add its value to the total score.
    for character in user_tiles_word:
        if character not in "?*":
            total_score += scores[character.lower()]
        else:
            continue
    return (total_score, scrabble_word)


def words_scores_lists(function, words_list):
    """ Uses the list of word pairs returned from `valid_words_list` and `score_word` to return a sorted list of our words 
    with their Scrabble score, sorted by score first then by alphabetical order.
    Args: Function (`score_word`) and a list of word pairs (String values)
    Returns: List of (word score, word) tuples for each valid word and the the length of the list (Integer)
            as a tuple. (word list, list length) """
    
    # Apply `score_word` (function) to the list of valid words (word_list) that `valid_words_list` returns to calculate 
    # the word score for each word in our list.
    words_scores = list(map(function, words_list))

    # Sort the list by the score value first, then by alphabetical order
    words_scores.sort(key = lambda tup: tup[0], reverse=True)
    return words_scores