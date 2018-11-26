from elo import rate_1vs1

result = rate_1vs1(800, 1200)
print(round(result[0]), round(result[1]))
result2 = rate_1vs1(1200, 800)
print(round(result2[0]), round(result2[1]))

"""
    Verbose Method of my function
"""
def add_differential(differentials, white_id, white_differential, black_id, black_differential):
    if white_id in differentials:
        differentials[white_id] = differentials[white_id] + white_differential
    else:
        differentials[white_id] = white_differential

    if black_id in differentials:
        differentials[black_id] = differentials[black_id] + black_differential
    else:
        differentials[black_id] = black_differential

    return differentials

def process_games(request, pk_club):
    club = get_object_or_404(Club, pk=pk_club)
    games = club.game_set.filter(processed=False).order_by('id')

    # Redirect if no games to process
    if not games:
        messages.warning(request, 'No games to process')
        return HttpResponseRedirect(reverse("club_games", args=(pk_club,)))

    # Results
    RESULTS = {
        0: "BLACK",
        1: "DRAW",
        2: "WHITE"
    }

    differentials = {}
    for game in games:
        print("Game ID")
        print(game.id)
        black_player = get_object_or_404(Player, pk=game.black_player.id)
        white_player = get_object_or_404(Player, pk=game.white_player.id)

        print(RESULTS[game.result])

        # Process the game
        if RESULTS[game.result] == "BLACK":
            print("BLACK WON")
            print("Black ID: ", black_player.id)
            print("White ID: ", white_player.id)
            print("Black Rating Before: ", black_player.rating)
            print("White Rating Before: ", white_player.rating)
            results = rate_1vs1(black_player.rating, white_player.rating)
            print(results)
            print("Black Rating After: ", round(results[0]))
            print("White Rating After: ", round(results[1]))
            print("DIFFERENTIAL")
            differential = {
                "black": {
                    "differential": round(results[0]) - black_player.rating,
                    "rating_before": black_player.rating,
                    "id": black_player.id
                },
                "white": {
                    "differential": round(results[1]) - white_player.rating,
                    "rating_before": white_player.rating,
                    "id": white_player.id
                }
            }
            # differential = json.dumps(differential)
            print(differential)
        elif RESULTS[game.result] == "WHITE":
            print("WHITE WON")
            print("Black ID: ", black_player.id)
            print("White ID: ", white_player.id)
            print("White Rating Before: ", white_player.rating)
            print("Black Rating Before: ", black_player.rating)
            results = rate_1vs1(white_player.rating, black_player.rating)
            print(results)
            print("White Rating After: ", round(results[0]))
            print("Black Rating After: ", round(results[1]))
            print("DIFFERENTIAL")
            differential = {
                "black": {
                    "differential": round(results[1]) - black_player.rating,
                    "rating_before": black_player.rating,
                    "id": black_player.id
                },
                "white": {
                    "differential": round(results[0]) - white_player.rating,
                    "rating_before": white_player.rating,
                    "id": white_player.id
                }
            }
            # differential = json.dumps(differential)
            print(differential)
        else:
            print("DRAWN")
            print("Black ID: ", black_player.id)
            print("White ID: ", white_player.id)
            print("White Rating Before: ", white_player.rating)
            print("Black Rating Before: ", black_player.rating)
            results = rate_1vs1(white_player.rating, black_player.rating)
            print(results)
            print("White Rating After: ", round(results[0]))
            print("Black Rating After: ", round(results[1]))
            print("DIFFERENTIAL")
            differential = {
                "black": {
                    "differential": round(results[1]) - black_player.rating,
                    "rating_before": black_player.rating,
                    "id": black_player.id
                },
                "white": {
                    "differential": round(results[0]) - white_player.rating,
                    "rating_before": white_player.rating,
                    "id": white_player.id
                }
            }
            # differential = json.dumps(differential)
            print(differential)

        # Add the differentials
        differentials = add_differential(differentials, white_player.id, differential["white"]["differential"], black_player.id, differential["black"]["differential"])
        print("Differentials")
        print(json.dumps(differentials))

        # Save the differential in the JSON column
        game.json = differential
        # Mark the game as processed
        game.processed = True
        game.save()

    # Update the player ratings
    for player_id, rating_differential in differentials.items():
        player = get_object_or_404(Player, pk=player_id)
        # Update the rating
        player.rating = player.rating + rating_differential
        player.save()

    # TODO - Save the differentials in a batch
    return HttpResponseRedirect(reverse("club_games", args=(pk_club,)))