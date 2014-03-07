'''Functions to calculate legal plays in Words with Friends.  The approach is
as follows.

1) for each position on the board, find all possible lengths of words which
begin on that square and which connect to the currently played tiles.

2) For each such length, find all words you can play that fill in a legal word
of that length starting in that position and which make a legal word in that
row.

3) For each tile you put down, check to make sure that the vertical words
formed are legal plays.

I believe that this search could be made smarter so as to take less time,
perhaps by starting from the currently played tiles and building words off of
them.  This will take a little more care to organize though.

'''

import re
from game_constants_wwf import *
from board_state import *

# The variables imported from board_state are BOARD, HAND and HAND_SIZE
# The variables imported from game_constants_wwf are TILE_VALUES,
# WORD_SCORE_MULTIPLIER and LETTER_SCORE_MULTIPLIER.

def allowable_lengths(position):
    '''Returns a list of the possible lengths that a word beginning at position
    can have.  Counts number of blank spaces to make sure you have enough tiles
    in hand to form the word.
    '''

    i, j = position
    row_length = len(BOARD[i])
    if j != 0 and BOARD[i][j-1] != ' ':
        return []
    else:
        count = 0
        if BOARD[i][j] == ' ':
            count += 1
        acceptable_lengths = []
        for k in range(j+1, row_length):
            if BOARD[i][k] == ' ':
                count += 1
            if k == row_length-1:
                if count:
                    acceptable_lengths.append(k-j+1)
                break
            if BOARD[i][k+1] == ' ':
                if count:
                    acceptable_lengths.append(k-j+1)
            if count == HAND_SIZE:
                break
        return [length for length in acceptable_lengths
                if has_neighbor(position, length)]


def has_neighbor(position, length):
    '''Boolean check whether a word beginning at position with this length will
    connect to the already played tiles on the board.'''

    i, j = position
    if (j != 0 and BOARD[i][j-1] != ' '
                or j != len(BOARD)-1 and BOARD[i][j+1] != ' '):
        return True
    for k in range(length):
        if (i != 0 and BOARD[i-1][j+k] != ' '
                    or i != len(BOARD[j+k])-1 and BOARD[i+1][j+k] != ' '):
            return True
    return False


def find_legal_plays(position, length):
    '''Return a list of the words of this length starting at position which
    can be played horizontally given the current BOARD state and your current
    HAND and for which all the vertically formed words are also legal.'''

    i, j = position
    hand_tiles = '['+''.join(HAND)+']'
    re_pattern = re.compile(
        '^'+''.join(map(lambda x: hand_tiles if x == ' ' else x,
        BOARD[i][j:j+length]))+'$')

    def enough_letters_checker(word):
        '''Boolean check if the word can be played with tiles in hand.'''

        my_letters = BOARD[i][j:j+length]+HAND
        return all([word.count(ch) <= my_letters.count(ch) for ch in set(word)])

    return [word for word in WORD_LIST
            if re_pattern.match(word)
            and vertical_word_checker(position, word)
            and enough_letters_checker(word)]


def vertical_word_checker(position, word):
    '''Boolean check if the vertical words formed by playing word at
    position are in the word list.'''

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
    '''Return the score for playing the given word starting at
    position.'''

    def iter_scorer(nexter, position, word, multiplier, score):
        '''Iterative form of the function. Schemey.'''

        if len(word) == 0:
            return multiplier*score
        return iter_scorer(
                    nexter,
                    nexter(position),
                    word[1:],
                    multiplier*word_score(position),
                    score+letter_score(position)*tile_score(word[0]))
    i, j = position
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
            score += iter_scorer(
                    lambda x: (x[0]+1, x[1]), (beg, j+k), side_word, 1, 0)
    return score


def letter_score(position):
    '''Double/Triple Letter Score multiplier.'''

    i, j = position
    if BOARD[i][j] != ' ':
        return 1
    return LETTER_SCORE_MULTIPLIER.get(position, 1)


def word_score(position):
    '''Double/Triple Word Score multiplier.'''

    i, j = position
    if BOARD[i][j] != ' ':
        return 1
    return WORD_SCORE_MULTIPLIER.get(position, 1)


def tile_score(tile):
    '''Point value for the letter ch.'''

    return TILE_VALUES[tile]


def list_plays_and_scores(position):
    '''Return a list of tuples of the form (score, word, position) which
    enumerate the possible legal horizontal plays and the corresponding
    score.'''

    play_score_list = []
    for length in allowable_lengths(position):
        play_score_list += [(score_play(position, play), play, position)
                            for play in find_legal_plays(position, length)]
    return play_score_list

def flip_board():
    '''Persistently flip global BOARD.  Enables the reuse of the above code to
    calculate vertical plays as well.'''

    global BOARD
    BOARD = [[BOARD[i][j] for i in range(len(BOARD))]
                                    for j in range(len(BOARD))]




