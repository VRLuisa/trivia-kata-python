import random

from trivia.game_old import GameOld


def read_yes_no():
    answer = input().strip().upper()

    if answer not in ["Y", "N"]:
        print("y or n please")
        return read_yes_no()

    return answer == "Y"


def read_roll():
    roll_text = input(">> Throw a die and input roll, or [ENTER] to generate a random roll: ").strip()

    if roll_text == "":
        roll = random.randint(1, 6)
        print(">> Random roll: " + str(roll))
        return roll

    if not roll_text.isdigit():
        print("Not a number: '" + roll_text + "'")
        return read_roll()

    roll = int(roll_text)

    if roll < 1 or roll > 6:
        print("Invalid roll")
        return read_roll()

    return roll


def main():
    print("*** Welcome to Trivia Game ***\n")
    print("Enter number of players: 1-4")

    player_count = int(input())

    if player_count < 1 or player_count > 4:
        raise ValueError("No player 1..4")

    print("Reading names for " + str(player_count) + " players:")

    game = GameOld()

    for i in range(1, player_count + 1):
        player_name = input("Player " + str(i) + " name: ")
        game.add(player_name)

    print("\n\n--Starting game--")

    not_a_winner = True

    while not_a_winner:
        roll = read_roll()
        game.roll(roll)

        print(">> Was the answer correct? [y/n] ", end="")
        correct = read_yes_no()

        if correct:
            not_a_winner = game.handleCorrectAnswer()
        else:
            not_a_winner = game.wrongAnswer()

    print(">> Game won!")


if __name__ == "__main__":
    main()