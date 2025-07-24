import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Setting up dataframe
df = pd.read_csv('tennis_atp/atp_matches_1968.csv')
for year in range(1969,2025):
    temp_df = pd.read_csv(f'tennis_atp/atp_matches_{year}.csv')
    df = pd.concat([df,temp_df])

# ========================= Wins by Surface =========================
surface_wins = df.groupby(['winner_name', 'surface']).size().unstack(fill_value=0)

surface_stats_df = pd.DataFrame(
    {"player": surface_wins.index,
    "hard_wins": surface_wins.get('Hard'),
    "grass_wins": surface_wins.get('Grass'),
    "clay_wins": surface_wins.get('Clay'),
    "carpet_wins": surface_wins.get('Carpet'),
    "total_wins": surface_wins.get('Hard') + surface_wins.get('Grass') + surface_wins.get('Clay') + surface_wins.get('Carpet')
    })
surface_stats_df = surface_stats_df.reset_index(drop=True)

# Top 20 players by wins for each surface
grass_stats = surface_stats_df.sort_values('grass_wins',ascending=False).iloc[:20,:]
clay_stats = surface_stats_df.sort_values('clay_wins',ascending=False).iloc[:20,:]
hard_stats = surface_stats_df.sort_values('hard_wins',ascending=False).iloc[:20,:]
total_stats = surface_stats_df.sort_values('total_wins',ascending=False).iloc[:20,:]

# Plotting each set of data
'''
grass_stats.plot(x='player', y='grass_wins', kind='bar',color='green',title='ATP Match Wins on Grass Courts (Open Era)')
plt.tight_layout()
clay_stats.plot(x='player', y='clay_wins', kind='bar',color='orange',title='ATP Match Wins on Clay Courts (Open Era)')
plt.tight_layout()
hard_stats.plot(x='player', y='hard_wins', kind='bar',color='blue',title='ATP Match Wins on Hard Courts (Open Era)')
plt.tight_layout()
total_stats.plot(x='player', y='total_wins', kind='bar',color='red',title='ATP Match Wins on All Courts (Open Era)')
plt.tight_layout()

plt.show()
'''

# ========================= Wins by Age =========================

# Average, oldest, and youngest age of ATP match winner
avg_win_age = df['winner_age'].mean()

oldest_win_age = df['winner_age'].max()
oldest_winner = df.loc[df['winner_age']==oldest_win_age]['winner_name']

youngest_win_age = df['winner_age'].min()
youngest_winner = df.loc[df['winner_age']==youngest_win_age]['winner_name']

# Boxplot for ages of ATP match winners
sns.set_theme(style='whitegrid')
fig1 = sns.boxplot(data=df['winner_age'],orient='h',width=.5,fliersize=2,linecolor="#000000",color="#C1024B")
fig1.set(title='Age of ATP Match Winners',ylabel='',xlabel='')
plt.show()


# ========================= Wins by Country =========================

# Ranking countries by # of ATP match wins
country_win_stats = df.groupby(['winner_ioc']).size().sort_values(ascending=False)
fig2 = sns.barplot(data=country_win_stats[:20],orient='h',color="#F63B11")
fig2.set(title='ATP Match Wins by Country',ylabel='Country',xlabel='# of Match Wins')
plt.show()

# Number of players from each country
df_players = pd.read_csv('tennis_atp/atp_players.csv')
players_per_country = df_players.groupby(['ioc']).size().sort_values(ascending=False)

other_players = players_per_country[15:].sum()
players_per_country = players_per_country[:14]
players_per_country.loc['Other'] = other_players

fig3 = players_per_country.plot(kind='pie', title='% of Players from each Country',colormap='magma')
plt.show()

