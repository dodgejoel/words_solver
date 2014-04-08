'''The main script which runs functions from play_finder_wwf and prints out the
results.'''

import play_finder_wwf

print('\nTOP SCORING HORIZONTAL AND VERTICAL PLAYS')
print('FORMAT = (score, word, starting (i, j) position)')

N = len(play_finder_wwf.BOARD)

HOR_PLAYS = []
for i in range(N):
    for j in range(N):
        HOR_PLAYS += play_finder_wwf.list_plays_and_scores((i, j))
HOR_PLAYS.sort()

print('\nHORIZONTAL PLAYS')
for i in HOR_PLAYS[-5:]:
    print(i)

play_finder_wwf.flip_board()
VER_PLAYS = []
for i in range(N):
    for j in range(N):
        VER_PLAYS += play_finder_wwf.list_plays_and_scores((i, j))
VER_PLAYS.sort()

print('\nVERTICAL PLAYS')
for i in VER_PLAYS[-5:]:
    i = (i[0], i[1], (i[2][1], i[2][0]))
    print(i)
