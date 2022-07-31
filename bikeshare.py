import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington)
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
        if city not in ('chicago', 'new york', 'washington'):
            print("Not an appropriate city! Please choose again")
        else:
            break
        
    # get user input for filter the data by month, day, both or not at all
    while True:
        filter_by = input('Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter\n').lower()
        if filter_by not in ('month', 'day', 'both', 'none'):
            print("Not an appropriate choice! Please choose again")
        else:
            break
            
    month = 'all'
    day = 'all'

    if filter_by in ('month', 'both'):
        # get user input for month (all, january, february, ... , june)
        while True:
            month = input('Which month - January, February, March, April, May, or June?\n').lower()
            if month not in ('january', 'february', 'march', 'april', 'may', 'june'):
                print("Not an appropriate month! Please choose again\n")
            else:
                break

    if filter_by in ('day', 'both'):
        # get user input for day of week (all, monday, tuesday, ... sunday)
        while True:
            day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').lower()
            if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                print("Not an appropriate day! Please choose again\n")
            else:
                break

    print('-'*40)
#     print(city, month, day)
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
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month.lower()) + 1
    
        # filter by month to create the new dataframe
        df = df.query("month == @month")

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the days list to get the corresponding int
        day = days.index(day.lower())
        # filter by day of week to create the new dataframe
        df = df.query("day_of_week == @day")


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    
    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month_name()
    popular_month = df['month'].mode()[0]

    # display the most common month
    print('Most common month:', popular_month)

    # extract day from the Start Time column to create a day column
    df['day'] = df['Start Time'].dt.day_name()
    popular_day = df['day'].mode()[0]
    
    # display the most common day of week
    print('Most common day of week:', popular_day)
    
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    # display the most common start hour
    print('Most common hour of day:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()


    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most common start station:', popular_start_station)


    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most common end station:', popular_end_station)


    # display most frequent combination of start station and end station trip
    df['Trip Stations'] = df['Start Station'].str.cat(df[['End Station']].values,sep=' -> ')
    popular_trip_station = df['Trip Stations'].mode()[0]
    print('Most common trip from start to end stations:', popular_trip_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time:', df['Trip Duration'].sum())

    # display mean travel time
    print('Average travel time:', df['Trip Duration'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of each user type
    user_types = df['User Type'].value_counts()
    print(user_types.to_string())
    
    # Display counts of each gender (only available for NYC and Chicago)
    if 'Gender' in df.columns:
        user_genders = df['Gender'].value_counts()
        print(user_genders.to_string())
    else:
        print('※ Gender column is not available')

    # Display earliest, most recent, most common year of birth (only available for NYC and Chicago)
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        print('Earliest birth year: ', earliest_birth_year)
        
        most_recent_birth_year = int(df['Birth Year'].max())
        print('Most recent birth year: ', most_recent_birth_year)

        most_birth_year = int(df['Birth Year'].mode()[0])
        print('Most common birth year: ', most_birth_year)
    else:
        print('※ Birth Year column is not available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """
    Display raw data upon request by the user in the following manner:
        Prompt the user if they want to see 5 lines of raw data,
        Display that data if the answer is 'yes',
        Continue iterating these prompts and displaying the next 5 lines of raw data at each iteration,
        Stop the program when the user says 'no' or there is no more raw data to display.
    """
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while (view_data == 'yes'):
        print(df.iloc[start_loc:start_loc+5])
        if (start_loc + 5 >= len(df.index)):
            print("No more data to view")
            break
        start_loc += 5
        view_data = input("Do you wish to continue? Enter yes or no\n").lower()
            
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
