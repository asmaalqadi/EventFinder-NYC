import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Key from .env 
TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY')
BASE_URL_DO_NYC = "https://donyc.com" # Taking the main url since it's adaptable

# Searching for events via Ticketmaster API on a given date
def search_events_from_ticketmaster(date):
    # Adjusted for potential timezone offset by starting from midnight of the given day
    start_date_str = datetime.combine(date, datetime.min.time()) + timedelta(hours=12)  # noon of the day to avoid time zone issues
    end_date_str = start_date_str + timedelta(days=1, seconds=-1)  # just before midnight of the same day
    start_date_iso = start_date_str.isoformat() + 'Z'
    end_date_iso = end_date_str.isoformat() + 'Z'
    
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={TICKETMASTER_API_KEY}&startDateTime={start_date_iso}&endDateTime={end_date_iso}&countryCode=US&city=New%20York"
    response = requests.get(url)
    if response.status_code == 200 and '_embedded' in response.json():
        events = response.json()['_embedded']['events']
        # Use the .get() method to safely access 'name' and 'url'
        return [{
            'Event Name': event.get('name', 'No Event Name Available'),  # Default if 'name' is missing
            'Link for Event': event.get('url', 'No URL Available')  # Default if 'url' is missing
        } for event in events]
    else:
        print(f"Error searching events from Ticketmaster: {response.status_code}, Response: {response.text}")
        return []
    
# Scrapes the 'Do NYC' website for events on a given date
def scrape_do_nyc(date):
    categories = ['music', 'comedy', 'food-wine-dining', 'film']
    date_str = date.strftime('%Y/%m/%d') # Making the date format same as the website
    url = f"{BASE_URL_DO_NYC}/events/{date_str}" # adding date to the base link
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser') # parsing html into a beautifulSoup object
    
    events = []
    for category in categories:
        class_selector = f'ds-listing event-card ds-event-category-{category}'
        for event in soup.find_all('div', class_=class_selector):
            title = event.find('span', class_='ds-listing-event-title-text').text.strip() if event.find('span', class_='ds-listing-event-title-text') else 'No Title Available'
            link = event.find('a', class_='ds-listing-event-title')['href'] if event.find('a', class_='ds-listing-event-title') else 'No Link Available'
            full_link = f"{BASE_URL_DO_NYC}{link}" if 'http' not in link else link
            events.append({
                'Event Name': title,
                'Link for Event': full_link,
                'Category': category  
            })
    return events

def get_most_common_category(events_df):
    if 'Category' in events_df.columns:
        return events_df['Category'].mode()[0]
    return "No category data"


def main():
    while True:
        try:
            print("Enter the date for which you want to search events (YYYY-MM-DD):")
            date_input = input()
            selected_date = datetime.strptime(date_input, '%Y-%m-%d')
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
    
    # Gets the  events from Ticketmaster APi
    tm_events = search_events_from_ticketmaster(selected_date)
    tm_events_df = pd.DataFrame(tm_events)

    # Scrapes the  events from 'Do NYC'
    donyc_events = scrape_do_nyc(selected_date)
    donyc_events_df = pd.DataFrame(donyc_events)

    # Combines both dataframes into one CSV file of all events 
    combined_df = pd.concat([tm_events_df, donyc_events_df], ignore_index=True, sort=False)
    if not combined_df.empty:
        # Save to CSV without the 'Category' column
        combined_df.drop(columns=['Category'], errors='ignore').to_csv('combined_events.csv', index=False)
        print("Combined events saved to 'combined_events.csv'.")
        
        # Determine the most common category
        most_common_category = get_most_common_category(donyc_events_df)
        print(f"The most common category on {selected_date.strftime('%Y-%m-%d')} is '{most_common_category}'.")
    else:
        print("No events found for the selected date.")

if __name__ == '__main__':
    main()
