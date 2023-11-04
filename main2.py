import config

import itertools

# configuration
league_position_in_yahoo_account = 0
week = 1

from yahoofantasy import Context, League

ctx = Context(client_id=config.yahoo_client_id, client_secret=config.yahoo_client_secret, refresh_token=config.refresh_token)
leagues = ctx.get_leagues('nfl', 2023)
# for league in leagues:
#     print(league.name + " -- " + league.id)

# league = League(ctx, leagues[league_pos].id)  # Use a manual league ID or get it from league.id above
league = next(lg for lg in leagues if lg.id == leagues[league_position_in_yahoo_account].id)

# for team in league.teams():
#     print(f"Team Name: {team.name}\tManager: {team.manager.nickname}")

#TODO: pull from Yahoo API
league_positions = {'QB': 2, 'WR': 3, 'RB': 3, 'TE': 2, 'W/R/T': 2, 'K': 1, 'DEF': 1} # , 'BN': 8, 'IR': 1

rosters = []


for team in league.teams():
    name = team.name
    print(name)
    roster = team.roster(week-1)
    lineup = []
    for player in roster.players:
        # print(f"{player.name.full} - {player.primary_position}/{player.selected_position.position} - {player.get_points(0)}")
        lineup.append({'name': player.name.full,
                       'position': player.primary_position,
                       'points': player.get_points(week-1)})
    rosters.append({'name': name,
                   'lineup': lineup})


# Create roster possiblities
league_possibilities = []
for roster in rosters:
    print(f'~~{roster["name"]}~~')
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
                position_possibilities.append({'name':player['name'], 'points':player['points']})
        print('poss',position_possibilities)
        roster_possibilities.append({'position':position, 'possibilities':position_possibilities})
    league_possibilities.append({'manager': roster['name'], 'possibilities': roster_possibilities})

# Create starting roster combinations
# combinations = list(itertools.combinations(my_list, 2)) (list, choose)

for manager in league_possibilities:
    for position_possibilities in manager['possibilities']:
        position_slots = league_positions[position_possibilities['position']]
        combinations = list(itertools.combinations(position_possibilities['possibilities'], position_slots))
        print(combinations)


    # Edit lists of combinations
        # Remove invalid combinations where players are in multiple slots (ex. WR and W/R/T)
        # Remove duplicate combinations where players are swapped slots (ex. WR in one combi and W/R/T in another)


# Calculate all possible scores

# Create graphs
# Histogram of possible scores
# Percentile of chosen roster
# Comparision in matchups

    # "name": player.name.full,
    # "week": week_num,
    # "manager": team.manager.nickname,
    # "team_id": team.id,
    # "position": player.primary_position,
    # "roster_position": player.selected_position.position,
    # "points": player.get_points(week_num),
#
# target_week = league.weeks()[week-1]
# for matchup in target_week.matchups:
#     print(f"{matchup.team1.name} vs {matchup.team2.name}")

