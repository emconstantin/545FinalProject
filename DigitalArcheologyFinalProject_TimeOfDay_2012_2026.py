# Converted from Jupyter Notebook


# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Use on_bad_lines='skip' to skip the malformed row near EOF after I recieved an error the first time
# Load data to dataframe for cleaning and analysis
traffic_data = pd.read_csv("export.csv", on_bad_lines='skip')
traffic_data.head()


# %%
# check for missing values by column

traffic_data.isna().sum()


# %%
# Check column data types to see if we need to adjust any of them
traffic_data.info()


# %% [markdown]
# # Data Cleaning


# %%
# change date of stop column to actual date data type instead of object
traffic_data['Date Of Stop'] = pd.to_datetime(traffic_data['Date Of Stop'], errors='coerce')


# %% [markdown]
# # Traffic Violations by Season
## ## We will use the meteorological seasons
## ### Source: https://www.timeanddate.com/calendar/aboutseasons.html
### Spring: March, April, May
## Summer: June, July, August
## Autumn (Fall): September, October, November
## Winter: December, January, February


# %%
# use .dt from pandas to extract month from date of stop
traffic_data['Month'] = traffic_data['Date Of Stop'].dt.month

# map month numbers to season mentioned above
def get_season(month):
    if pd.isna(month):
        return None
    if month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Autumn'
    else:
        return 'Winter'

# add season column using mappings
traffic_data['Season'] = traffic_data['Month'].apply(get_season)

# filter and make a dataframe to keep only unique SeqID entries
unique_stops = traffic_data.drop_duplicates(subset=['SeqID']).dropna(subset=['Season'])

# count number of stops by season
season_counts = unique_stops['Season'].value_counts()
display(season_counts.to_frame('Unique Stops'))


# %%
# plot bar plot to visualize stops by season
plt.figure(figsize=(8, 5))
sns.barplot(x=season_counts.index, y=season_counts.values, palette='viridis', hue=season_counts.index, legend=False)
plt.title('Number of Traffic Stops in Mongomery County by Season')
plt.xlabel('Season')
plt.ylabel('Number of Stops')
plt.show()


# %% [markdown]
# # Traffic stops trend from 2012-2026


# %%
# get year from date of stop column
traffic_data['Year_Of_Stop'] = traffic_data['Date Of Stop'].dt.year

# filter for unique stops using SeqID and years >= 2012
unique_stops_by_year = traffic_data.drop_duplicates(subset=['SeqID']).dropna(subset=['Year_Of_Stop'])
unique_stops_since_2012 = unique_stops_by_year[unique_stops_by_year['Year_Of_Stop'] >= 2012]

# count unique stops per year
yearly_counts = unique_stops_since_2012['Year_Of_Stop'].value_counts().sort_index()

# table of stops by year
display(yearly_counts.to_frame('Unique Stops'))

# plot line graph
plt.figure(figsize=(10, 5))
sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, marker='o', color='b', linewidth=2)
plt.title('Trend of Traffic Stops in Montgomery County Since 2012')
plt.xlabel('Year')
plt.ylabel('Number of Stops')
plt.grid(True, alpha=0.5)
plt.xticks(yearly_counts.index, rotation=45)
plt.show()


# %%



# %% [markdown]
# # Traffic Stops by Time of Day (2012–2026)
## Morning: 6 AM–11:59 AM; Afternoon: 12 PM–5:59 PM; Evening: 6 PM–11:59 PM; Night: 12 AM–5:59 AM.



# %%
# Extract the year and hour of each stop
traffic_data['Year_Of_Stop'] = traffic_data['Date Of Stop'].dt.year

# Check the time column name in the exported dataset
print([column for column in traffic_data.columns if 'time' in column.lower()])
time_column = 'Time Of Stop'

# Parse clock times, including HH:MM and HH:MM:SS formats
stop_times = pd.to_datetime(traffic_data[time_column].astype('string').str.strip(), format='%H:%M:%S', errors='coerce')
missing_times = stop_times.isna()
stop_times.loc[missing_times] = pd.to_datetime(
    traffic_data.loc[missing_times, time_column].astype('string').str.strip(),
    format='%H:%M', errors='coerce'
)
traffic_data['Hour_Of_Stop'] = stop_times.dt.hour

def get_time_of_day(hour):
    if pd.isna(hour):
        return None
    if 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 18:
        return 'Afternoon'
    elif 18 <= hour < 24:
        return 'Evening'
    else:
        return 'Night'

traffic_data['Time_Of_Day'] = traffic_data['Hour_Of_Stop'].apply(get_time_of_day)

# Count unique stops for each year and time-of-day category
unique_stops_time = traffic_data.drop_duplicates(subset=['SeqID']).dropna(
    subset=['Year_Of_Stop', 'Time_Of_Day']
).copy()
unique_stops_time = unique_stops_time[
    unique_stops_time['Year_Of_Stop'].between(2012, 2026)
]

period_order = ['Morning', 'Afternoon', 'Evening', 'Night']
time_of_day_counts = (
    unique_stops_time.groupby(['Year_Of_Stop', 'Time_Of_Day'])
    .size()
    .unstack(fill_value=0)
    .reindex(index=range(2012, 2027), columns=period_order, fill_value=0)
)
time_of_day_counts.index.name = 'Year'
display(time_of_day_counts)



# %%
# Compare the time-of-day distribution across years
plt.figure(figsize=(12, 6))
sns.lineplot(data=time_of_day_counts, markers=True, dashes=False)
plt.title('Traffic Stops in Montgomery County by Time of Day (2012–2026)')
plt.xlabel('Year')
plt.ylabel('Number of Unique Stops')
plt.xticks(range(2012, 2027), rotation=45)
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.show()



# %%
# Compare time-of-day patterns as percentages within each year
percent_by_year = time_of_day_counts.div(
    time_of_day_counts.sum(axis=1).replace(0, float('nan')), axis=0
).mul(100)
display(percent_by_year.round(1))

percent_by_year.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Share of Traffic Stops by Time of Day (2012–2026)')
plt.xlabel('Year')
plt.ylabel('Percentage of Unique Stops')
plt.legend(title='Time of Day', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.show()

