
import itertools
import yahoo_fantasy_api as yfa

from yahoo_oauth import OAuth2


sc = OAuth2(None, None, from_file='oauth2.json')
gm = yfa.Game(sc, 'nfl')
lg = gm.to_league(gm.league_ids(year=2023)[0])

print(lg.stat_categories())