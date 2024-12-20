import numpy
import sklearn.metrics
import tensorflow
import sklearn.ensemble
import sklearn.model_selection
import sklearn
import statsapi
import data.mlb_data
import pickle
import pandas as pd


def train_model():
    df = pd.read_csv('hard_data_copy.csv', index_col='game_id')
    X = []
    y = []
    for index, row in df.iterrows():
        t1 = row['team1']
        t1_list = eval(t1)
        t2 = row['team2']
        t2_list = eval(t2)
        X.append([t1_list[1], t1_list[5], t1_list[8], t1_list[9], t1_list[11], t1_list[12], t1_list[16], t1_list[19], t1_list[32],
                  t2_list[1], t2_list[5], t2_list[8], t2_list[9], t2_list[11], t2_list[12], t2_list[16], t2_list[19], t2_list[32]])
        y.append(row['team_1_win'])

    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.2)
    rf = sklearn.ensemble.RandomForestClassifier(n_estimators=10000, min_samples_leaf=150)
    print('start training')
    rf.fit(X_train, y_train)
    score3 = rf.score(X_test, y_test)
    score4 = rf.score(X_train, y_train)
    print('test:', score3)
    print('train', score4)
    filename = 'randomforest_model.sav'
    pickle.dump(rf, open(filename, 'wb')) 
    


def get_all_games(year):
    games = statsapi.schedule(start_date=f'1/1/{year}', end_date=f'12/31/{year}')
    return [(x['home_id'], x['away_id'], x['home_score'], x['away_score'], x['game_date']) for x in games]


def get_data(homeID, awayID, game_date):
    return data.mlb_data.get_team_stats(homeID, awayID, 10, game_date)


if __name__ == '__main__':
    train_model()
