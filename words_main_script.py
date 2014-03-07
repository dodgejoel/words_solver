import play_finder_wwf

N = len(play_finder_wwf.BOARD)

hor_plays = []
for i in range(N):
    for j in range(N):
        hor_plays += play_finder_wwf.list_plays_and_scores((i, j))
hor_plays.sort()

print('HORIZONTAL PLAYS')
for i in hor_plays:
    print(i)

play_finder_wwf.flip_board()
ver_plays = []
for i in range(N):
    for j in range(N):
        ver_plays += play_finder_wwf.list_plays_and_scores((i, j))
ver_plays.sort()

print('VERTICAL PLAYS')
for i in ver_plays:
    i = (i[0], i[1], (i[2][1], i[2][0]))
    print(i)
