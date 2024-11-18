import pickle
import statsapi
import os
import pandas as pd
import datetime
import model_training.data.mlb_data as mlb_data



#-----------Average Team Stats--------------------
# Check if ststs can be obtained for a certain date (before a match we want to predict)

#a = statsapi.get('stats', {'stats': 'season', 'group': 'hitting', 'teamId': 121, 'season':2024})
#for i in a['stats'][0]['splits'][0]['stat']:
#    print(i, a['stats'][0]['splits'][0]['stat'][i])



#------------------Singular games?------------------------
#s = statsapi.schedule(team=133, start_date='01/01/2023', end_date='12/31/2023')
#w = sum(1 for x in s if x.get('winning_team','')=='Oakland Athletics')
#print(w/len(s))

#s = statsapi.schedule(start_date='01/01/2023', end_date='12/31/2023', team=133)
#print(len(s))
#print(s[0])
#print(s[-1])



#------------------Single Game stats--------------------------
#b = statsapi.boxscore_data(719496)
#for _ in b:
#    print(_, b[_])
#    print()



#------------------Average League Stats (All Teams)
#t = statsapi.game_pace_data()
#print(t)



# matchup between team 1 team 2
# repeat. Lookup games from past year (months)
# stats api . schedule start end date
# grab last 10   schedule[-10:]
# get stats from last 10 games + winner
# feed into machine
# done

#print(statsapi.schedule(date='2024-9-11'))

#data = statsapi.schedule(game_id=746831)
#print(data)
#wt = data[0]['winning_team']
#print(wt)
#a = statsapi.lookup_team('Athletics')
#print(a)
#for i in data:
#    print(i, data[i])
#    print()


#a = statsapi.schedule(start_date=f'1/1/2024', end_date=f'12/31/2024')
#print(a[0])

#games = statsapi.schedule(start_date=f'1/1/2024', end_date=f'12/31/2024')
#for x in games:
#    print(x['game_id'])
#    print(x['home_id'], x['away_id'], x['winning_team'], x['game_date'])


#problem = statsapi.lookup_team(133)
#print(problem)





#1wins at index 32, 2 at 65

#games = statsapi.schedule(start_date=f'1/1/2024', end_date=f'12/31/2024')
#all_game_ids = [x['game_id'] for x in games]
#df = pd.read_csv('hard_data_copy.csv', index_col='game_id')
#
#row = df.loc[745848]
#print(row)

#for index, row in df.iterrows():
#    print('index:', index)
#    print('row:', row)
#    t1 = row['team1']
#    t2 = row['team2']
#    print(t1+t2)
#    break


random_forest_model = pickle.load(open('randomforest_model.sav', 'rb'))
data = mlb_data.get_team_stats(143, 144, 10, datetime.datetime.today().date().strftime('%Y-%m-%d'))
if data is not None:
    inputs = [
        data[0][1], data[0][5], data[0][8], data[0][9], data[0][11], data[0][12], data[0][16], data[0][19], data[0][32],
        data[1][1], data[1][5], data[1][8], data[1][9], data[1][11], data[1][12], data[1][16], data[1][19], data[1][32]
        ]
    prediction = random_forest_model.predict_proba([inputs])
    print(prediction[0][0])

