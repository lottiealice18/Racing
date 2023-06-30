import pandas as pd
import numpy as np
import streamlit as st

# Read the Excel file and drop rows where Country is South Africa
df = pd.read_excel('C:/Users/liamh/PycharmProjects/Football/Football_Data/RDB_20230626.xlsx')
df = df[df['Country'] != 'South Africa']

# Convert date column to datetime type
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')

# Format date column as "DD/MM/YYYY"
df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')
# Race types and class options (used in multiple functions)
race_types = [
    'Selling Stakes',
    'Claiming Stakes',
    'Selling Handicap',
    'Nursery',
    'Maiden',
    'Amateur',
    'Group 1',
    'Group 2',
    'Group 3',
    'Other Handicap',
    'Classified Stakes',
    'Conditions Stakes',
    'Novice Stakes',
    'NH Flat',
    'Novice Hcap Hurdle',
    'Novice Hcap Chase',
    'Hunters Chase',
    'Handicap Hurdle',
    'Novice Hurdle',
    'Handicap Chase',
    'Novice Chase',
    'Listed',
    'Selling Hurdle',
    'Other Chase',
    'Other Hurdle',
    'Unclassified'
]

class_options = sorted(df['Class'].dropna().unique())

# Function to display main data
def display_main_data():
    # Sort the DataFrame by 'Time' column in ascending order
    df_sorted = df.sort_values(by='Time')

    # Display the race cards in time order
    st.dataframe(df_sorted)

    # Download link for CSV
    csv = df_sorted.to_csv(index=False)
    st.download_button(
        label='Download Todays Full Race Card as CSV',
        data=csv,
        file_name='todays_full_race_card.csv',
        mime='text/csv'
    )


def display_horses_last_n_days():
    # Convert 'Date Last Run' column to numeric
    df['Date Last Run'] = pd.to_numeric(df['Date Last Run'], errors='coerce')

    # Filter out rows where 'Date Last Run' is NaN
    df_filtered = df[df['Date Last Run'].notnull()]

    # Calculate the maximum number of days since the last run
    max_days = df_filtered['Date Last Run'].max()
    max_days = int(max_days) if pd.notnull(max_days) else 1

    # User input for number of days
    n_days = st.number_input('Enter the maximum number of days since the last run', min_value=1, max_value=int(max_days), value=int(max_days), help='Enter a number between 1 and the maximum number of days available.')

    # Filter the DataFrame for horses that ran in the last N days
    df_lastNdays = df_filtered[df_filtered['Date Last Run'] <= n_days]

    # Rename the column to 'Days Since Last Run'
    df_lastNdays = df_lastNdays.rename(columns={'Date Last Run': 'Days Since Last Run'})

    # Sort the DataFrame by 'Days Since Last Run' column in descending order
    df_lastNdays = df_lastNdays.sort_values(by='Days Since Last Run', ascending=False)

    # Description of 'Days Since Last Run' page and how filters work
    st.write('This page displays horses that have run in the last N days. Enter the maximum number of days since the last run using the number input above, and the table will show horses that have run within that time period. The table is sorted by default based on the days since the last run in descending order.')

    # Display the filtered DataFrame
    st.dataframe(df_lastNdays)

    # Download link for CSV
    csv = df_lastNdays.to_csv(index=False)
    st.download_button(
        label='Download CSV',
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv'
    )

# Function to display race data
def display_race_data():
    # Create radio buttons for venue selection
    selected_venue = st.radio('Select Venue', df['Venue'].unique())

    # Filter the DataFrame based on the selected venue
    df_filtered_venue = df[df['Venue'] == selected_venue]

    # Create dropdown for race times
    race_times = df_filtered_venue['Time'].unique()
    race_times_with_view_all = np.append(race_times, 'View All Races')
    selected_time = st.selectbox('Select Race Time', race_times_with_view_all)

    # Filter the DataFrame based on the selected venue and time
    if selected_time == 'View All Races':
        df_filtered_race = df_filtered_venue
    else:
        df_filtered_race = df_filtered_venue[df_filtered_venue['Time'] == selected_time]

    # Display the races at the selected venue
    if len(df_filtered_race) > 0:
        st.dataframe(df_filtered_race)
    else:
        st.write("No races available for the selected venue and time.")

    # Download link for the selected race as a CSV
    if selected_time != 'View All Races' and len(df_filtered_race) > 0:
        csv_race = df_filtered_race.to_csv(index=False)
        st.download_button(
            label='Download Race CSV',
            data=csv_race,
            file_name='race_data.csv',
            mime='text/csv'
        )

    # Download link for all races at the selected venue as a CSV
    csv_all_races = df_filtered_venue.to_csv(index=False)
    st.download_button(
        label='Download All Races at Venue CSV',
        data=csv_all_races,
        file_name='all_races_data.csv',
        mime='text/csv'
    )


# Function to display class data
def display_class_data():
    # Radio buttons for class selection
    selected_class = st.radio('Select Class', class_options)

    if selected_class:
        # Filter the DataFrame based on selected class
        df_filtered = df[df['Class'] == selected_class]

        if len(df_filtered) > 0:
            # Get unique race times
            race_times = df_filtered['Time'].unique()

            # Sort the race times in ascending order
            sorted_race_times = np.sort(race_times)

            for time in sorted_race_times:
                # Filter the DataFrame for the selected race time
                df_race = df_filtered[df_filtered['Time'] == time]

                # Display the race title
                st.subheader(f"Race at {time}")

                # Display the DataFrame of horses in the selected class and race time
                st.dataframe(df_race)

                # Download link for CSV
                csv = df_race.to_csv(index=False)
                st.download_button(
                    label=f'Download Race {time} CSV',
                    data=csv,
                    file_name=f'race_{time}_data.csv',
                    mime='text/csv'
                )
        else:
            st.write("No horses found in the selected class.")

        # Download link for CSV
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label='Download CSV',
            data=csv,
            file_name='class_data.csv',
            mime='text/csv'
        )

    else:
        st.write("Please select a class.")

# New function to display change of class information
# New function to display change of class information
def change_of_class():
    # Display description
    st.write("This page provides information about changes in class for each race. The 'Class Change' column in the data indicates any changes in class for the horses in a race. Class changes can provide insights into the competitiveness and level of competition in a race.")

    # Get unique options from the "Class Change" column and sort them in ascending order
    class_changes = sorted(df['Class Change'].unique())

    # Create radio buttons for class change selection
    selected_change = st.radio('Select Class Change', class_changes)

    # Filter the DataFrame based on the selected class change
    df_filtered_change = df[df['Class Change'] == selected_change]

    # Display the races with the selected class change
    if len(df_filtered_change) > 0:
        st.dataframe(df_filtered_change)
    else:
        st.write("No races available for the selected class change.")

    # Download link for the selected class change races as a CSV
    csv_change = df_filtered_change.to_csv(index=False)
    st.download_button(
        label='Download Class Change Races CSV',
        data=csv_change,
        file_name='class_change_races.csv',
        mime='text/csv'
    )


# Function to display race type data
def display_race_type_data():
    # Determine which race names are in the DataFrame
    current_race_names = df['Race Name'].unique()

    # Calculate the intersection of all possible race types and the current race names
    intersect_race_types = [race_type for race_type in race_types if any(race_type in race_name for race_name in current_race_names)]

    # Multi-select dropdown for race types
    selected_race_types = st.multiselect('Select Race Types', intersect_race_types)

    if selected_race_types:
        # Filter the DataFrame based on selected race types
        df_filtered = df[df['Race Name'].str.contains('|'.join(selected_race_types), na=False)]

        if len(df_filtered) > 0:
            # Sort the filtered DataFrame by 'Time' column in ascending order
            df_filtered = df_filtered.sort_values(by='Time')

            # Display the DataFrame of races matching the selected race types
            st.write("Races:")
            st.dataframe(df_filtered)
        else:
            st.write("No races found for the selected race types.")

        # Download link for CSV
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label='Download CSV',
            data=csv,
            file_name='race_type_data.csv',
            mime='text/csv'
        )

    else:
        st.write("Please select race types.")

# Function to find and display races with the lowest weight horses
def find_lowest_weight_horses(df):
    df = df[df['Country'] != 'South Africa']

    df['Weight'] = pd.to_numeric(df['Weight'], errors='coerce')
    grouped = df.groupby('Time')

    # We'll store the races (DataFrames) in this list to display in Streamlit
    races = []

    for time, data in grouped:
        sorted_data = data.sort_values('Weight')

        lowest_weight_horse = sorted_data.iloc[0]
        lowest_weight = lowest_weight_horse['Weight']

        if sorted_data[sorted_data['Weight'] == lowest_weight].shape[0] > 1:
            continue

        if sorted_data['Weight'].nunique() == 1:
            continue

        next_horse = sorted_data.iloc[1]
        weight_difference = next_horse['Weight'] - lowest_weight

        if weight_difference >= 0.5:
            races.append(sorted_data)

    return races
def horse_search():
    # Read the CSV file and drop rows where Country is South Africa
    df = pd.read_csv(r'C:\Users\liamh\OneDrive\Desktop\Stats & Systems\All Years Combined - Clean.csv')
    df = df[df['Country'] != 'South Africa']

    # User input for horse name
    horse_name = st.text_input("Enter the horse's name:", value='', help='Enter the name of the horse you want to search for.')
    horse_name = horse_name.strip()  # Trim white spaces
    horse_name = horse_name.title()  # Convert to title case to handle case sensitivity

    if horse_name:  # If the horse name is not empty
        # Filter the DataFrame for races that the specified horse has run in
        df_horse = df[df['Horse'].str.contains(horse_name, case=False, na=False)]  # Use 'case=False' to make the search case-insensitive

        if len(df_horse) > 0:
            st.subheader(f"Horse: {horse_name}")
            st.dataframe(df_horse)

            # Generate download link for CSV
            csv_horse = df_horse.to_csv(index=False)
            st.download_button(
                label=f'Download {horse_name} Races CSV',
                data=csv_horse,
                file_name=f'{horse_name.replace(" ", "_").replace("/", "_")}_races_data.csv',
                mime='text/csv'
            )
        else:
            st.write("No data available for the specified horse.")

    else:
        st.write("Please enter a horse name.")


def display_top_speed():
    # Filter the DataFrame for races that have a top speed rating
    df_top_speed = df[df['Top Speed'] != '-']
    df_top_speed = df_top_speed.dropna(subset=['Top Speed'])

    if len(df_top_speed) > 0:
        # Convert 'Top Speed' column to numeric type
        df_top_speed['Top Speed'] = pd.to_numeric(df_top_speed['Top Speed'])

        # Find the horse(s) with the maximum top speed for each race
        top_speed_horses = df_top_speed.groupby('Race Name').apply(lambda x: x.loc[x['Top Speed'].idxmax()]).reset_index(drop=True)
        top_speed_horses = top_speed_horses[['Time', 'Horse', 'Venue', 'Date', 'Top Speed', 'Jockey', 'Trainer']]

        if len(top_speed_horses) > 0:
            # Sort the DataFrame by 'Time' column
            top_speed_horses = top_speed_horses.sort_values('Time')

            st.dataframe(top_speed_horses)

            # Generate download link for CSV
            csv_data = top_speed_horses.to_csv(index=False)
            st.download_button(
                label='Download Top Speed Horses CSV',
                data=csv_data,
                file_name='top_speed_horses.csv',
                mime='text/csv'
            )
        else:
            st.write("No top speed horses found.")
    else:
        st.write("No data available for top speeded horses.")


def filter_rank():
    # Read historical data
    df_hist = pd.read_excel(r'C:\Users\liamh\Downloads\RDB_20230624.xlsx')

    # Convert date column to datetime type
    df_hist['Date'] = pd.to_datetime(df_hist['Date'], format='%Y%m%d')

    # Format date column as "DDMMYYYY"
    df_hist['Date'] = df_hist['Date'].dt.strftime('%d/%m/%Y')

    # Filter the DataFrame for races that have a rank
    df_rank = df_hist[(df_hist['WFF Rank'] == 1) & (df_hist['RDB Rank'] == 1)]

    if len(df_rank) > 0:
        st.dataframe(df_rank)

        # Download link for CSV
        csv_filtered = df_rank.to_csv(index=False)
        st.download_button(
            label='Download Filtered Data CSV',
            data=csv_filtered,
            file_name='filtered_data.csv',
            mime='text/csv'
        )
    else:
        st.write("No data available for the selected rank.")

# Function to search data by filters (Trainer and Jockey)
def search_by_trainer():
    # User input for Trainer filter
    trainers = [''] + sorted(df['Trainer'].unique())
    selected_trainer = st.selectbox("Select Trainer:", trainers, help="Filter by trainer")

    # Filter the DataFrame based on the selected trainer
    if selected_trainer:
        df_filtered = df[df['Trainer'] == selected_trainer]

        st.dataframe(df_filtered)

        # Provide option to download filtered data
        csv_filtered_data = df_filtered.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data CSV",
            data=csv_filtered_data,
            file_name="filtered_data.csv",
            mime="text/csv"
        )
def jockey_search():
    # User input for Jockey filter
    jockeys = [''] + sorted(df['Jockey'].unique())
    selected_jockey = st.selectbox("Select Jockey:", jockeys, help="Filter by jockey")

    # Filter the DataFrame based on the selected jockey
    if selected_jockey:
        df_filtered = df[df['Jockey'] == selected_jockey]

        st.dataframe(df_filtered)

        # Provide option to download filtered data
        csv_filtered_data = df_filtered.to_csv(index=False)
        st.download_button(
            label="Download Filtered Data CSV",
            data=csv_filtered_data,
            file_name="filtered_data.csv",
            mime="text/csv"
        )


# Function to display data based on surface type
def display_surface_type_data():
    # Determine unique surface types from the 'Surface Type' column
    surface_types = df['Surface Type'].unique()

    # Create radio buttons for surface type selection
    selected_surface_type = st.radio('Select Surface Type', surface_types)

    # Filter the DataFrame based on the selected surface type
    df_filtered = df[df['Surface Type'] == selected_surface_type]

    if len(df_filtered) > 0:
        # Display the filtered DataFrame
        st.dataframe(df_filtered)

        # Download link for CSV
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label='Download CSV',
            data=csv,
            file_name='surface_type_data.csv',
            mime='text/csv'
        )
    else:
        st.write("No races found for the selected surface type.")

# Function to display data based on handicap category
def display_handicap_data():
    # Filter the DataFrame for races categorized as 'Handicap' or 'Non Handicap'
    selected_handicap = st.radio('Select Handicap Category', ['Y', 'N'])
    df_handicap = df[df['Handi/Non Handi'] == selected_handicap]

    if len(df_handicap) > 0:
        # Display the filtered DataFrame
        st.dataframe(df_handicap)

        # Download link for CSV
        csv = df_handicap.to_csv(index=False)
        st.download_button(
            label='Download CSV',
            data=csv,
            file_name='handicap_data.csv',
            mime='text/csv'
        )
    else:
        st.write("No races found for the selected Handicap category.")

# Function to display data based on race category (Flat or Jump)
def display_race_category_data():
    # Create radio buttons for race category selection
    selected_race_category = st.radio('Select Race Category', ['Flat', 'Jump'])

    # Filter the DataFrame based on the selected race category
    df_race_category = df[df['Race Name'].str.contains(selected_race_category, na=False, case=False, regex=True)]

    if len(df_race_category) > 0:
        # Display the filtered DataFrame
        st.dataframe(df_race_category)

        # Download link for CSV
        csv = df_race_category.to_csv(index=False)
        st.download_button(
            label='Download CSV',
            data=csv,
            file_name='race_category_data.csv',
            mime='text/csv'
        )
    else:
        st.write("No races found for 'Flat/Jump' category.")


def display_course_and_distance():
    st.write("This page allows filtering races based on Course and Distance Filters. You can select: Course Winner, Distance Winner, and/or Course & Distance Winner.")

    # Create multi-select checkboxes for winner types
    selected_winners = st.multiselect("Select Winner Types", ['Course Winner', 'Distance Winner', 'Course & Distance Winner'])

    # Filter the DataFrame based on the selected winner types
    if 'Course Winner' in selected_winners:
        df_filtered = df[df['Course Winner'] == 'Y']
    elif 'Distance Winner' in selected_winners:
        df_filtered = df[df['Distance Winner'] == 'Y']
    elif 'Course & Distance Winner' in selected_winners:
        df_filtered = df[df['Course & Distance Winner'] == 'Y']
    else:
        df_filtered = pd.DataFrame()

    if len(df_filtered) > 0:
        st.dataframe(df_filtered)
    else:
        st.write("No races available for this Filter.")
