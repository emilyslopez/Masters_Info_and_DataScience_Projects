""" 
The Cheating at Scrabble Program contains two modules: this main program (scrabble.py) and wordscore.py.

scrabble.py imports functions from wordscore.py to run the scrabble program. The function defined in this program is 
`run_scrabble` which takes a Scrabble rack of size 2 to 7 as an input and uses the tiles (chracters A-Z, * and ?) to
return all possible combinations of valid Scrabble English words along with their scrabble score and the total number of possible
words.

This program uses data from "sowpods.txt." It contains all of the "valid Scrabble English" words from the official words list. It
also uses the predefined "scores" dictionary which has letters as keys and their Scrabble points as values.

Example:

# "ZAEfiee" is our Scrabble rack
run_scrabble("ZAEfiee") -> (
[(17, 'FEAZE'),
(17, 'FEEZE'),
(16, 'FAZE'),
(15, 'FEZ'),
(15, 'FIZ'),
(12, 'ZEA'),
(12, 'ZEE'),
(11, 'ZA'),
(6, 'FAE'),
(6, 'FEE'),
(6, 'FIE'),
(5, 'EF'),
(5, 'FA'),
(5, 'FE'),
(5, 'IF'),
(2, 'AE'),
(2, 'AI'),
(2, 'EA'),
(2, 'EE')], 
19
)

Example with wildcard:

run_scrabble("?F") -> (
[(4, 'EF'),
(4, 'FA'),
(4, 'FE'),
(4, 'FY'),
(4, 'IF'),
(4, 'OF')],
6
)
"""

import wordscore as ws

def run_scrabble(input_tiles):
    """ Given a list of characters (tiles in the Scrabble rack), prints all "valid Scrabble English" 
    words that can be constructed from that rack, along with their Scrabble scores, sorted by score. 
    Args: Scrabble rack/list of character tiles as a String
    Returns: List of (score, word) Tuples and the total number of valid words as an Integer"""

    # Check that amount of input tiles is within 2-7
    if len(input_tiles) < 2 or len(input_tiles) > 7:
        return f"A Scrabble rack is made up of 2 to 7 tiles.\nYou entered {len(input_tiles)} tile(s). Please input 2 to 7 tiles only."
    
    # Check that the input does not have more than one * or ? (can have max one and one)
    if input_tiles.count("*") > 1 or input_tiles.count("?") > 1:
        return f"The maximum number of wildcards ('*' and '?') that can be in a rack is 2, one of each character.\
                     \nPlease make sure your amount of wildcards is valid.\nInvalid: '??' and '**' \nValid: '*?' and '?*' "
    
    # Check that the input only contains letters and/or wildcards (*, ?)
    rack = input_tiles.upper()
    check_validity = [True if tile in "ABCDEFGHIJKLMNOPQRSTUVWXYZ?*" else False for tile in rack]
    if False in check_validity:
       invalid_tiles = [input_tiles[idx] for idx, i in enumerate(check_validity) if i is False]
       return f"A Scrabble rack can only have letters or wildcards (*, ?).\
                     \nYou entered these invalid tiles: {', '.join(invalid_tiles)}"
    
    # If all tiles are valid, continue with the cheating at scrabble program and return a tuple: 
    # (sorted list of words and their score, total number of valid words)
    else:
        words_scores = ws.words_scores_lists(ws.score_word, ws.valid_words_list(rack))
        return (words_scores, len(words_scores))
