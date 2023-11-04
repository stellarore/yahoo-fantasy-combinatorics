
import itertools
import yahoo_fantasy_api as yfa
from yahoo_oauth import OAuth2

# configuration
league = 0
week = 1



sc = OAuth2(None, None, from_file='oauth2.json')
gm = yfa.Game(sc, 'nfl')
lg = gm.to_league(gm.league_ids(year=2023)[league])
tms = lg.teams()

positions = lg.positions()
print("__postions settings__")
# print(positions)
position_dict = {}
for key in positions:
    position_dict[key] = positions[key]['count']
    print(f"{key}: {positions[key]['count']}")
print(position_dict)

print("__get rosters__")
if False:
    for team_id in tms:
        tm = lg.to_team(team_id)
        opponent = tm.matchup(week)
        print(f"{tms[team_id]['name']} vs. {tms[opponent]['name']}")
        print(tm.roster(week))

# print(lg.player_stats([32671],'week',week=1))
# print(lg.player_details([32671]))