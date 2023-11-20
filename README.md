# Achievements_Dashboard
Dashboard to centralize a users achievements across multiple platforms, allowing the user to see aggregated statistics or breakdown by platform.

Currently, this project only supports the Steam platform with Playstation and Xbox as future integrations. 

## Features

### Steam Profile Demographics
Displays basic public information of a users account:
*   Total games owned
*   Total Achivements Earned
*   Percentage of achieved achievments in users library
*   Table Showing an entire users game library breaking down playtime and achievements earned

![img](data\images\steam_demographics.png)

## CMI
Launch the ,dashboard
> streamlit run main.py

Initalize a SQL database
> sqlite3 data\Achievements.db < data\schema.sql