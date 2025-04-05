import requests
import pandas as pd
import numpy as np
import json

def parse_data_and_add_to_csv(output_file_path, inning, over, ball, hawkID):
    columns = ['country','format','batting_team','bowling_team','home_for_bat','home_for_bowl','batter','bat_id','bat_hand',
                'nonstriker','nonstriker_hand','bowler','bowler_id','innings','ball_id','over_num','ball_num','ball_type','runs','boundary','extras','extras_type',
                'is_wicket','wicket_type','wickets_taken','shot_attack','shot_played','shot_type_additional',
                'bounce_angle','bounce_x','bounce_y','bounce_z','cof','cor','crease_x','crease_y','crease_z','deviation','drop_angle','hit_stumps',
                'impact_x','impact_y','impact_z','react_time_to_crease','react_time_to_intercept','pbr','release_speed',
                'release_x','release_y','release_z','initial_angle','swing','stump_x','stump_y','stump_z']

    BASE_URL = "https://polls.iplt20.com/widget/welcome/get_data"

    url = f"{BASE_URL}?path=Delivery_{inning}_{over}_{ball}_{hawkID}.json"

    try:
        response = requests.get(url, timeout = 100)
        data = response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")

    if not data:
        #print('skipped iteration')
        return
    
    #output_file_path = 'hawkeye_data.json'
        
    #try:
     #   with open(output_file_path, 'w', encoding='utf-8') as json_file:
      #      json.dump(data, json_file, indent=4)  # indent=4 for pretty printing
       #     #print(f"Successfully wrote JSON data to {output_file_path}")
    #except Exception as e:
     #   print(f"Error writing JSON file: {str(e)}")
        
    #with open('hawkeye_data.json', 'r') as file:
    #initialise all the subdictionaries required
    match_data = data['match']
    batting_team_data = match_data['battingTeam']
    bowling_team_data = match_data['bowlingTeam']
    batter_data = batting_team_data['batsman']
    nonstriker_data = batting_team_data['batsmanPartner']
    bowler_data = bowling_team_data['bowler']
    deliveryInfo = match_data['delivery']
    ball_trajectory = deliveryInfo['trajectory']
    bounce = ball_trajectory['bouncePosition']
    stump = ball_trajectory['stumpPosition']
    crease = ball_trajectory['creasePosition']
    impact = ball_trajectory['impactPosition']
    release = ball_trajectory['releasePosition']
    shot_info = deliveryInfo['shotInformation']
    score_info = deliveryInfo['scoringInformation']
    wicket_info = score_info['wicket']
    delivery_num = deliveryInfo['deliveryNumber']

    #extract data to be put into CSV
    country = data['country']
    format = data['format']
    batting_team = batting_team_data['name']
    bowling_team = bowling_team_data['name']
    home_for_bat = batting_team_data['home']
    home_for_bowl = bowling_team_data['home']
    batter = batter_data['name']
    bat_id = batter_data['id']
    bat_hand = 'RHB'
    if batter_data['isRightHanded'] == 'false':
        bat_hand = 'LHB'
    nonstriker = nonstriker_data['name']
    nonstriker_hand = 'RHB'
    if nonstriker_data['isRightHanded'] == 'false':
        nonstriker_hand = 'LHB'
    bowler = bowler_data['name']
    bowler_id = bowler_data['id']
    innings = delivery_num['innings']
    over_num = delivery_num['over']
    ball_num = delivery_num['ball']
    ball_type = deliveryInfo['deliveryType']
    ball_id = f'{over_num-1}.{ball_num}'
    print(f"innings: {innings}, ball: {ball_id}")
    runs = score_info['score']
    boundary = score_info['boundary']
    extras = score_info['extrasScore']
    extras_type = score_info['extrasType']
    is_wicket = wicket_info['isWicket']
    wicket_type = wicket_info['wicketType']
    wickets_taken = wicket_info['wicketsTaken']
    shot_attack = shot_info['shotAttacked']
    shot_played = shot_info['shotPlayed']
    shot_type_additional = shot_info['shotTypeAdditional']

    bounce_angle = ball_trajectory['bounceAngle']
    bounce_x = bounce['x']
    bounce_y = bounce['y']
    bounce_z = bounce['z']

    cof = ball_trajectory['cof']
    cor = ball_trajectory['cor']
    crease_x = crease['x']
    crease_y = crease['y']
    crease_z = crease['z']

    deviation = ball_trajectory['deviation']
    drop_angle = ball_trajectory['dropAngle']
    hit_stumps = ball_trajectory['hitStumps']
    impact_x = impact['x']    
    impact_y = impact['y']
    impact_z = impact['z']


    react_time_to_crease = ball_trajectory['reactionTime(to crease)']
    react_time_to_intercept = ball_trajectory['reactionTime(to interception)']
    pbr = ball_trajectory['pbr']
    release_speed = ball_trajectory['releaseSpeed']
    release_x = release['x']
    release_y = release['y']
    release_z = release['z']
    swing = ball_trajectory['swing']
    initial_angle = ball_trajectory['initialAngle']
    stump_x = stump['x']
    stump_y = stump['y']
    stump_z = stump['z']

    #construct single list of all values to be written to csv
    output_data_to_csv = [country, format,batting_team,bowling_team,home_for_bat,home_for_bowl,batter,bat_id,bat_hand,
                          nonstriker,nonstriker_hand,bowler,bowler_id,innings,ball_id,over_num,ball_num,ball_type,runs,boundary,extras,extras_type,
                          is_wicket,wicket_type,wickets_taken,shot_attack,shot_played,shot_type_additional,
                          bounce_angle,bounce_x,bounce_y,bounce_z,cof,cor,crease_x,crease_y,crease_z,deviation,drop_angle,hit_stumps,
                          impact_x,impact_y,impact_z,react_time_to_crease,react_time_to_intercept,pbr,release_speed,
                          release_x,release_y,release_z,initial_angle,swing,stump_x,stump_y,stump_z]
    #print(output_data_to_csv)
    
    output_df = pd.DataFrame([output_data_to_csv],columns=columns)
    if innings == 1 and over == 1 and ball == 1:
        output_df.to_csv(output_file_path,index=False)
        #print('file_created')
    else:
        output_df.to_csv(output_file_path, mode='a', header=False, index=False)
        #print('file appended')

if __name__ == "__main__":
    output_file_path = 'yourfile.csv'
    hawkID = 00000 #fill the match ID for which you would like to extract data
    for innings in range(1,3):
        for over in range(1,21):
            for ball in range(1,10):   #ball range is kept till 10 here to account for extras. You can increase this in case, a particular over in a match has more than 3 extras
                parse_data_and_add_to_csv(output_file_path, innings, over, ball, hawkID)
