import config

import itertools
from yahoofantasy import Context
# import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import math
import time

# configuration
league_position_in_yahoo_account = 0
week = 1


ctx = Context(client_id=config.yahoo_client_id, client_secret=config.yahoo_client_secret, refresh_token=config.refresh_token)
leagues = ctx.get_leagues('nfl', 2023)
# for league in leagues:
#     print(league.name + " -- " + league.id)

# league = League(ctx, leagues[league_pos].id)  # Use a manual league ID or get it from league.id above
league = next(lg for lg in leagues if lg.id == leagues[league_position_in_yahoo_account].id)

# for team in league.teams():
#     print(f"Team Name: {team.name}\tManager: {team.manager.nickname}")

# TODO: pull from Yahoo API
league_positions = {'QB': 2, 'WR': 3, 'RB': 3, 'TE': 2, 'W/R/T': 2, 'K': 1, 'DEF': 1}  # , 'BN': 8, 'IR': 1

start = time.perf_counter()
rosters = []

def no_dupe_checker(flex, wr, rb, te):
    for rb_dup in rb:
        if flex['name'] == rb_dup['name']:
            return False
    for wr_dup in wr:
        if flex['name'] == wr_dup['name']:
            return False
    for te_dup in te:
        if flex['name'] == te_dup['name']:
            return False
    return True

print("Loading Rosters")
for team in league.teams():
    name = team.name
    # print(name)
    roster = team.roster(week-1)
    lineup = []
    for player in roster.players:
        # print(f"{player.name.full} - {player.primary_position}/{player.selected_position.position} - {player.get_points(0)}")
        lineup.append({'name': player.name.full,
                       'position': player.primary_position,
                       'points': player.get_points(week-1)})
    rosters.append({'name': name,
                   'lineup': lineup})

print("Listing valid positions")
# Create roster possibilities
league_possibilities = []
for roster in rosters:
    # print(f'~~{roster["name"]}~~')
    roster_possibilities = []
    for position in league_positions:
        # print(position)
        position_possibilities = []
        for player in roster['lineup']:
            # print(player)
            if position == 'W/R/T':
                if player['position'] in ['WR', 'RB', 'TE']:
                    position_possibilities.append({'name': player['name'], 'points': player['points']})
            elif player['position'] == position:
                position_possibilities.append({'name': player['name'], 'points': player['points']})
        roster_possibilities.append({'position': position, 'possibilities': position_possibilities})
    league_possibilities.append({'manager': roster['name'], 'possibilities': roster_possibilities})

# Create starting roster combinations,
# Edit lists of combinations
        # Remove invalid combinations where players are in multiple slots (ex. WR and W/R/T)
        # Remove duplicate combinations where players are swapped slots (ex. WR in one combi and W/R/T in another)
# Calculate all possible scores

# combinations = list(itertools.combinations(my_list, 2)) (list, choose)

print("Making roster combinations, calculating scores")
league_combinations = {}
for manager in league_possibilities:
    position_combinations = {}
    for position_possibilities in manager['possibilities']:
        position_slots = league_positions[position_possibilities['position']]
        combinations = list(itertools.combinations(position_possibilities['possibilities'], position_slots))
        position_combinations[position_possibilities['position']] = combinations

    roster_combinations = []
    point_combinations = []
    # Nested for loops to collect all roster combinations
    if True:
        for qb in position_combinations["QB"]:
            for rb in position_combinations["RB"]:
                for wr in position_combinations["WR"]:
                    for te in position_combinations["TE"]:
                        for k in position_combinations["K"]:
                            for defense in position_combinations["DEF"]:
                                for wrt in position_combinations["W/R/T"]:
                                    for flex in wrt: # check if any flex players are duplicating
                                        if no_dupe_checker(flex, rb, wr, te):
                                            # roster_combinations.extend(sorted([list(qb) + list(rb) + list(wr) + list(te) + list(wrt) + list(k) + list(defense)]))
                                            roster_combinations.append(sorted([list(qb) + list(rb) + list(wr) + list(te) + list(wrt) + list(k) + list(defense)]))

        # [print(i) for i in roster_combinations[0:4]]
        combination_set = list(roster_combinations for roster_combinations,_ in itertools.groupby(roster_combinations)) # remove slot swapping duplicates
        for combination in combination_set:
            x = [player['points'] for position in combination for position in combination]
            point_combinations.append(sum([player['points'] for position in combination for player in position])) # flattens list and sums only points

        # all combinations for single manager tabulated
        print(manager['manager'], "\t", len(roster_combinations), len(combination_set))
        # [print(i) for i in combination_set[0:4]]
        # print(point_combinations[0:20])

        # s = pd.Series(point_combinations)
        # print(s.describe())

        if True:
            league_combinations[manager['manager']] = point_combinations


        # [ QB(AB, AC), WR (11, 12), RB (ZY, ZX)...]
        """
        967680
        882000
        3427200
        1814400
        1209600
        1234800"""
stop = time.perf_counter()

print(list(league_combinations.keys()))

print("time", stop - start)
print("Graphs and Statistics")
# Create graphs
# Histogram of possible scores
# Percentile of chosen roster
# Comparison in matchups

    # "name": player.name.full,
    # "week": week_num,
    # "manager": team.manager.nickname,
    # "team_id": team.id,
    # "position": player.primary_position,
    # "roster_position": player.selected_position.position,
    # "points": player.get_points(week_num),
target_week = league.weeks()[week-1]

for matchup in target_week.matchups:
    print(f"{matchup.team1.name} vs {matchup.team2.name}")
    print(f"{matchup.teams.team[0].team_points.total} - {matchup.teams.team[1].team_points.total}")
    matchup_points = [matchup.teams.team[0].team_points.total, matchup.teams.team[1].team_points.total]

    arr1 = np.array(league_combinations[str(matchup.team1.name)])
    arr2 = np.array(league_combinations[str(matchup.team2.name)])
    arr = np.concatenate((arr1, arr2), axis=None)

    bins = np.linspace(math.ceil(min(arr)),
                       math.floor(max(arr)),
                       20)  # fixed number of bins

    plt.xlim([min(arr) - 5, max(arr) + 5])

    plt.hist(arr1, bins=bins, alpha=0.5, label=matchup.team1.name)
    plt.hist(arr2, bins=bins, alpha=0.5, label=matchup.team2.name)

    plt.axvline(x=matchup_points[0])
    plt.axvline(x=matchup_points[1])

    plt.title(f'{matchup.team1.name} vs {matchup.team2.name}- Week {week}')
    plt.xlabel('Points')
    plt.ylabel('Number of Roster Combinations')

    plt.show()

