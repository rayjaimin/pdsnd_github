from ast import While
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

ALL = 'all'
MONTHS = [ 'january', 'february', 'march', 'april', 'may', 'june' ]
DAYS = [ 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday' ]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        print('Please enter the city to analyze (chicago, new york city, washington)')
        city = input().lower()
        if city in CITY_DATA:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        print('Please enter name of the month to filter (all, january, february, march, april, may, june)')
        month = input().lower()
        if month == 'all' or month in MONTHS:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print('Please enter name of the day to filter (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)')
        day = input().lower()
        if day == 'all' or day in DAYS:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if 'month' in df.columns:
        common_month = df['month'].mode()[0]
        print('most common month:', MONTHS[common_month - 1].title())

    # display the most common day of week
    if 'day_of_week' in df.columns:
        common_day = df['day_of_week'].mode()[0]
        print('most common day:', common_day.title())

    # display the most common start hour
    if 'Start Time' in df.columns:
        df['start hour'] = df['Start Time'].dt.hour
        print('most common start hour:', df['start hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    if 'Start Station' in df.columns:
        common_start_station = df['Start Station'].mode()[0]
        print('most common start station: ', common_start_station.title())

    # display most commonly used end station
    if 'End Station' in df.columns:
        common_end_station = df['End Station'].mode()[0]
        print('most common end station: ', common_end_station.title())

    # display most frequent combination of start station and end station trip
    if df.columns.isin({ 'Start Station' , 'End Station'}).all():
        common_pair = df.groupby('Start Station')['End Station'].value_counts().idxmax()
        print('most common pair: ', common_pair)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # if Trip Duration is present
    if 'Trip Duration' in df.columns:
        # display total travel time
        print('total travel time: ', df['Trip Duration'].sum())

        # display mean travel time
        print('mean travel time: ', df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        print('user types count: ', df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print('gender counts: ', df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        df['Birth Year'] = pd.to_numeric(df['Birth Year'])
        print('most earliest year: ', df['Birth Year'].min())
        print('most recent year: ', df['Birth Year'].max())
        print('most common year: ', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    idx = 0
    # till user says "no" or we have data
    while True:
        print('Do you want to see 5 lines of raw data? (yes, no)')
        res = input().lower()
        # break on "no"
        if res == 'no':
            break
        # show data on yes
        if res == 'yes':
            # print first 5 records
            print(df.head())
            while True:
                print('Do you want to see next 5 lines of the data? (yes, no)')
                nested_res = input().lower()
                length_of_records = len(df.index)
                if nested_res == 'no':
                    break
                elif nested_res == 'yes':
                    idx += 5
                    print(df[idx: idx + 5])
                    if idx >= length_of_records:
                        break
            break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
