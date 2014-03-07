import re
from game_constants_wwf import *
from game1 import *

# The variables imported from board_hand_data are BOARD, HAND and HAND_SIZE

# The variables imported from game_constants_wwf are TILE_VALUES,
# WORD_SCORE_MULTIPLIER and LETTER_SCORE_MULTIPLIER.

def allowable_lengths(position):
    '''Returns a list of the possible lengths that a word beginning at position
    can have.  Counts number of blank spaces to make sure you have enough tiles
    in hand to form the word.  It's not clear to me that there isn't an easier
    way to do this.  This is just an implementation of the most obvious method
    for finding which lengths are possible.
    
    BOARD and HAND_SIZE are both global variables.
    '''

    i, j = position
    row_length = len(BOARD[i])
    if j != 0 and BOARD[i][j-1] != ' ':
        return []
    else:
        count = 0
        if BOARD[i][j] == ' ':
            count += 1
        acceptable_lengths=[]
        for k in range(j+1, row_length):
            if BOARD[i][k] == ' ':
                count += 1
            if k == row_length-1:
                acceptable_lengths.append(k-j+1)
                break
            if BOARD[i][k+1] == ' ':
                acceptable_lengths.append(k-j+1)
            if count == HAND_SIZE:
                break

        # add code to make sure that this length of word will lead to a
        # connected board.  OK to assume that the board was already connected.  

        return [length for length in acceptable_lengths if has_neighbor(position, length)]

def has_neighbor(position, length):
    i, j = position
    if j!= 0 and BOARD[i][j-1] != ' ' or j != len(BOARD)-1 and BOARD[i][j+1] != ' ':
        return True
    for k in range(length):
        if i!= 0 and BOARD[i-1][j+k] != ' ' or i != len(BOARD[j+k])-1 and BOARD[i+1][j+k] != ' ':
            return True
    return False



def find_legal_plays(position, length):
    '''Return a list of all the words of given length starting at position which
    can be played horizontally given the current BOARD state and your current
    HAND and for which all the vertically formed words are also legal.'''

    i, j = position
    hand_tiles = '['+''.join(HAND)+']'
    re_pattern = re.compile(
        '^'+''.join(map(lambda x: hand_tiles if x == ' ' else x,
        BOARD[i][j:j+length]))+'$')
    
    def enough_letters_checker(word):
        my_letters = BOARD[i][j:j+length]+HAND
        return all([word.count(ch) <= my_letters.count(ch) for ch in set(word)])
    
    return [word for word in WORD_LIST if re_pattern.match(word)
        and vertical_word_checker(position, word) and enough_letters_checker(word)] 
    


def vertical_word_checker(position, word):
    '''Return true if all of the vertical words formed by playing word at
    position are in the word list.  Return False otherwise.'''

    i, j = position
    for k in range(len(word)):
        if BOARD[i][j+k] == ' ':
            column = [BOARD[m][j+k] for m in range(len(BOARD))]
            column[i] = word[k]
            if not all([word in WORD_LIST or len(word) == 1 for word in 
                        ''.join(column).split()]):
                return False
    return True



def score_play(position, word):
    '''Return the score for playing the given word horizontally starting at
    position.'''
   
    # this function does not compute the correct score.  Need to figure out
    # where the bug is.  Distinction between k and j+k is all fucked up.
    # Can sort this out when I have a minute.  Scoring plays is so fucking
    # hard!

    def iter_scorer(nexter, position, word, multiplier, score):
        if len(word) == 0:
            return multiplier*score
        return iter_scorer(
                    nexter,
                    nexter(position),
                    word[1:],
                    multiplier*word_score(position),
                    score+letter_score(position)*tile_score(word[0]))
    i,j = position
    score = 0
    score += iter_scorer(lambda x: (x[0], x[1]+1), position, word, 1, 0)
    for k in [m for m in range(len(word)) if BOARD[i][j+m] == ' ']:
        beg = i
        end = i
        while beg != 0 and BOARD[beg-1][j+k] != ' ':
            beg -= 1
        while end != len(BOARD)-1 and BOARD[end+1][j+k] != ' ':
            end += 1
        if beg != end:
            column = [BOARD[m][j+k] for m in range(len(BOARD))]
            column[i] = word[k]
            side_word = ''.join([column[m] for m in range(beg, end+1)])
            score += iter_scorer(lambda x: (x[0]+1, x[1]), (beg, j+k), side_word, 1, 0)
    return score

def word_score(position):
    i, j = position
    if BOARD[i][j] != ' ':
        return 1
    return WORD_SCORE_MULTIPLIER.get(position, 1)

def tile_score(ch):
    return TILE_VALUES[ch]

def letter_score(position):
    i, j = position
    if BOARD[i][j] != ' ':
        return 1
    return LETTER_SCORE_MULTIPLIER.get(position, 1)

def list_plays_and_scores(position):
    '''Return a list of tuples of the form (score, word, position) which
    enumerate the possible legal horizontal plays and the corresponding
    score.'''
    
    play_score_list = []
    for length in allowable_lengths(position):
        play_score_list += [(score_play(position, play), play, position) 
                            for play in find_legal_plays(position, length)]
    return play_score_list
