import play_finder_wwf

N = len(play_finder_wwf.BOARD)
plays = []
for i in range(N):
    for j in range(N):
        plays += play_finder_wwf.list_plays_and_scores((i, j))
plays.sort()
for i in plays:
    print(i)
