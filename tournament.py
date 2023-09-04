import csv
import sys
import random

N = 1000

def simulate_game(team1, team2):
    rating_diff = team1["rating"] - team2["rating"]
    probability = 1 / (10 ** (-rating_diff / 600) + 1)
    return random.random() < probability

def simulate_round(teams):
    winners = []
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])
    return winners

def simulate_tournament(teams):
    while len(teams) > 1:
        teams = simulate_round(teams)
    return teams[0]["team"]

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILE")

    filename = sys.argv[1]

    teams = []

    with open(filename) as file:
        reader = csv.DictReader(file)
        for row in reader:
            team = {
                "team": row["team"],
                "rating": int(row["rating"])
            }
            teams.append(team)

    counts = {}

    for _ in range(N):
        winner = simulate_tournament(teams)
        if winner in counts:
            counts[winner] += 1
        else:
            counts[winner] = 1

    total_simulations = N
    probabilities = {}

    for team, count in counts.items():
        probability = count / total_simulations * 100
        probabilities[team] = probability

    sorted_probabilities = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)

    for team, probability in sorted_probabilities:
        print(f"{team}: {probability:.1f}% chance of winning")

if __name__ == "__main__":
    main()
    