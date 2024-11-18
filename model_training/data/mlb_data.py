import statsapi
import pandas as pd
import numpy as np
import datetime


def main(year):
    all_games = get_all_games(year)
    counter = 1
    all_data = []
    for game in all_games:
        try:
            dat = get_team_stats(game[0], game[1], 10, game[4])
        except Exception:
            print('Exception at game:', game)
            continue
        print('Done', counter, 'out of', len(all_games), '.\t', datetime.datetime.now().time().strftime('%H:%M.%S'))
        counter += 1
        if dat is not None:
            y = 0
            #winner = get_winning_team_id(game[2])
            if game[2] >= game[3]:
                y = 1
            try:
                all_data.append(
                    (game[5],
                    {
                        'team1':dat[0],
                        'team2':dat[1],
                        'team_1_win':y
                    }
                ))
            except Exception:
                print('Error in append at game', game)
                continue
        break
    #df = pd.DataFrame([x[1] for x in all_data], index=[y[0] for y in all_data])
    #df.index.name = 'game_id'
    #df.to_csv('data.csv')
        

def get_all_games(year):
    games = statsapi.schedule(start_date=f'1/1/{year}', end_date=f'12/31/{year}')
    return [(x['home_id'], x['away_id'], x['home_score'], x['away_score'], x['game_date'], x['game_id']) for x in games]


def get_team_stats(team1_ID, team2_ID, game_amt, game_date):
    team1_games = get_last_x_games(team1_ID, game_amt, game_date)
    team1_stats = get_game_stats(team1_ID, team1_games, True)
    team2_games = get_last_x_games(team2_ID, game_amt, game_date)
    team2_stats = get_game_stats(team2_ID, team2_games, False)

    if team1_stats == -1 or team2_stats == -1:
        return None
    return (team1_stats, team2_stats)


def get_last_x_games(teamID, game_amt, game_date):
    d = datetime.datetime.strptime(game_date, '%Y-%m-%d').strftime('%m/%d/%Y')
    new_date = datetime.datetime.strptime(d, '%m/%d/%Y')
    start_date = (new_date - datetime.timedelta(days=365)).strftime('%m/%d/%Y')
    end_date = (new_date - datetime.timedelta(days=1)).strftime('%m/%d/%Y')
    #print(start_date)
    games = statsapi.schedule(team=teamID, start_date=start_date, end_date=end_date)
    return [x['game_id'] for x in games[-game_amt:]]


def get_game_stats(teamID, gameIDs, first_team):
    team_num = '1'
    if not first_team:
        team_num = '2'
    game_count = len(gameIDs)
    if game_count == 0:
        print('team: ', teamID)
        return -1
    total_stats_dict = {}
    total_stats_dict[f'{team_num}wins'] = 0
    averaged_stats_list = []
    for gameID in gameIDs:
        #print(gameID)
        data = statsapi.boxscore_data(gameID)
        #print(data)
        if data['home']['team']['id'] == teamID:
            teamha = 'home'
        elif data['away']['team']['id'] == teamID:
            teamha = 'away'
        else:
            print('Error')
            game_count -= 1
            continue
        for stat in data[teamha]['teamStats']['batting']:
            if (f'{team_num}b_' + stat) in total_stats_dict.keys():
                total_stats_dict[f'{team_num}b_' + stat] += float(data[teamha]['teamStats']['batting'][stat])
            else:
                total_stats_dict[f'{team_num}b_' + stat] = float(data[teamha]['teamStats']['batting'][stat])
        for stat in data[teamha]['teamStats']['pitching']:
            if (f'{team_num}p_' + stat) in total_stats_dict.keys():
                total_stats_dict[f'{team_num}p_' + stat] += float(data[teamha]['teamStats']['pitching'][stat])
            else:
                total_stats_dict[f'{team_num}p_' + stat] = float(data[teamha]['teamStats']['pitching'][stat])        
        if total_stats_dict[f'{team_num}b_runs'] > total_stats_dict[f'{team_num}p_runs']:
            total_stats_dict[f'{team_num}wins'] += 1
    for entry in total_stats_dict:
        total_stats_dict[entry] = float(total_stats_dict[entry]/game_count)
    sorted_keys = sorted(total_stats_dict.keys())
    for val in sorted_keys:
        #print(val)
        averaged_stats_list.append(total_stats_dict[val])
    return averaged_stats_list


if __name__ == '__main__':
    main(2024)