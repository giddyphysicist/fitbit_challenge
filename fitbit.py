#fitbit.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



df_ttm_steps = pd.read_csv('./ToTheMax_StepChallenge - Steps.csv').iloc[:14,:]
df_ttm_active = pd.read_csv('./ToTheMax_StepChallenge - Active Minutes.csv').iloc[:14,:]

df_wd_steps = pd.read_csv('./WalkingDead_StepChallenge - Steps.csv').iloc[:14,:]
df_wd_active = pd.read_csv('./WalkingDead_StepChallenge - Active Minutes.csv').iloc[:14,:]

df_wd_steps

def to_numeric(number_string):
    if isinstance(number_string,str):
        number = float(number_string.replace(',',''))
    else:
        number = float(number_string)
    return number

def get_daily_score_per_person(number_of_steps, 
                               number_of_active_minutes, 
                               norm_steps=10_000, 
                               norm_active = 22, 
                               const_coefficient = 500):
    number_of_steps = to_numeric(number_of_steps)
    number_of_active_minutes = to_numeric(number_of_active_minutes)
    
    
    step_component = float(number_of_steps) / norm_steps
    active_component = float(number_of_active_minutes) / norm_active
    
    if np.isnan(step_component):
        step_component = 0.0
    
    if np.isnan(active_component):
        active_component = 0.0
    
    if step_component == 0 and active_component == 0:
        return np.nan    
    daily_score = int(const_coefficient * (step_component + active_component))

    return daily_score

def get_players(df):
    return [x for x in df.columns if x not in ('Date', 'Day')]

def get_scores_for_player(player, df_steps, df_active, norm_steps, norm_active,const_coefficient):
    steps = df_steps[player].values
    actives = df_active[player].values
    result = [get_daily_score_per_person(step,active,norm_steps, norm_active,const_coefficient) for step,active in zip(steps,actives)]
    return result

def get_team_player_scores(df_steps, df_active,norm_steps=10_000,norm_active=22,const_coefficient=500):
    score_records = {}
    for player in get_players(df_steps):
        scores = get_scores_for_player(player, df_steps, df_active,norm_steps,norm_active,const_coefficient)
        score_records[player] = scores
    return score_records

def get_avg_team_score_per_day(score_records):
    return np.nanmean(np.array(list(score_records.values())).T,1)

def plot_avg_daily_score_per_team(norm_steps=10_000, norm_active=22, const_coefficient=500):
    short_date = [x[:4] for x in df_wd_steps.Date.values]
    wd_scores = get_team_player_scores(df_wd_steps, df_wd_active,norm_steps,norm_active,const_coefficient)
    ttm_scores = get_team_player_scores(df_ttm_steps, df_ttm_active,norm_steps,norm_active,const_coefficient)
    wd_avg_scores = get_avg_team_score_per_day(wd_scores)
    ttm_avg_scores = get_avg_team_score_per_day(ttm_scores)
    plt.figure(figsize=(10,8))
    plt.plot(short_date,wd_avg_scores,'o-',label='Walking Dead Avg. Score')
    plt.plot(short_date,ttm_avg_scores,'o-', label='To The Max Avg. Score')
    plt.legend(loc='best')
    plt.title(f'norm_steps={norm_steps}, norm_active={norm_active},coeff={const_coefficient}')
    plt.xlabel('Date')
    plt.ylabel('Avg. Team Score')
    plt.show()
    
def plot_cumulative_avg_daily_score_per_team(norm_steps=10_000, norm_active=22, const_coefficient=500):
    short_date = [x[:4] for x in df_wd_steps.Date.values]
    wd_scores = get_team_player_scores(df_wd_steps, df_wd_active,norm_steps,norm_active,const_coefficient)
    ttm_scores = get_team_player_scores(df_ttm_steps, df_ttm_active,norm_steps,norm_active,const_coefficient)
    wd_avg_scores = get_avg_team_score_per_day(wd_scores)
    ttm_avg_scores = get_avg_team_score_per_day(ttm_scores)
    plt.figure(figsize=(10,8))
    plt.plot(short_date,np.cumsum(wd_avg_scores),'o-',label='Walking Dead Avg. Score')
    plt.plot(short_date,np.cumsum(ttm_avg_scores),'o-', label='To The Max Avg. Score')
    plt.legend(loc='best')
    plt.title(f'norm_steps={norm_steps}, norm_active={norm_active},coeff={const_coefficient}')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Avg. Team Score')
    plt.show()

def get_avg_daily_score_per_team(norm_steps=10_000, 
                                 norm_active=22, 
                                 const_coefficient=500,
                                 df_wd_steps=df_wd_steps,
                                 df_wd_active=df_wd_active):
    short_date = [x[:4] for x in df_wd_steps.Date.values]
    wd_scores = get_team_player_scores(df_wd_steps, df_wd_active,norm_steps,norm_active,const_coefficient)
    ttm_scores = get_team_player_scores(df_ttm_steps, df_ttm_active,norm_steps,norm_active,const_coefficient)
    wd_avg_scores = get_avg_team_score_per_day(wd_scores)
    ttm_avg_scores = get_avg_team_score_per_day(ttm_scores)
    x1 = short_date
    y1 = wd_avg_scores
    y2 = ttm_avg_scores
    return {'date':x1,'wd':y1,'ttm':y2}

def get_cumulative_avg_daily_score_per_team(norm_steps=10_000, 
                                            norm_active=22, 
                                            const_coefficient=500,
                                            df_wd_steps=df_wd_steps,
                                            df_wd_active=df_wd_active,
                                            df_ttm_steps=df_ttm_steps,
                                            df_ttm_active=df_ttm_active):
    short_date = [x[:4] for x in df_wd_steps.Date.values]
    wd_scores = get_team_player_scores(df_wd_steps, df_wd_active,norm_steps,norm_active,const_coefficient)
    ttm_scores = get_team_player_scores(df_ttm_steps, df_ttm_active,norm_steps,norm_active,const_coefficient)
    wd_avg_scores = get_avg_team_score_per_day(wd_scores)
    ttm_avg_scores = get_avg_team_score_per_day(ttm_scores)
    x1 = short_date
    y1 = np.cumsum(wd_avg_scores)
    y2 = np.cumsum(ttm_avg_scores)
    return {'date':x1,'Walking Dead Score':y1,'To The Max Score':y2}

NORM_STEPS = 10_000 #(sigma)
NORM_ACTIVE = 22 #(alpha)


# plot_avg_daily_score_per_team(norm_steps=NORM_STEPS, norm_active=NORM_ACTIVE)
# plot_cumulative_avg_daily_score_per_team(norm_steps=NORM_STEPS, norm_active=NORM_ACTIVE)