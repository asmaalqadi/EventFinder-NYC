# Event Finder in NYC

## Project Overview

EventFinder-NYC is a tool that outputs a wide variety of events in New York City from both Ticketmaster and Do NYC. Unlike traditional event finders that only focus on major, globally popular events, EventFinder-NYC brings together everything from large concerts and sports games to smaller, more niche local events. Whether you're looking for the next big concert or a unique community event, EventFinder-NYC gathers all relevant event information in one convenient place.

## Features

- **Comprehensive Event Variety**: By combining events from both Ticketmaster and Do NYC, this tool provides access to a diverse selection of events and returns the most common cateogry of the chosen day. Users can explore both mainstream and niche events without the hassle of visiting multiple websites.
- **User Input**: Allows users to input a specific date to retrieve events happening on that day. This feature enables precise searching that tailors the output to the user's specific needs.
- **Automated Scraping**: Utilizes BeautifulSoup to scrape Do NYC for localized events and the Ticketmaster API to gather event information from larger venues and major events. This automation ensures that the data is always up to date and comprehensive.
- **Unified Event Output**: Merges data from both sources and presents event names and links in a single, comprehensive list, offering a complete picture of what's happening in NYC. This unified view makes it easier for users to discover and decide on events to attend.
- **CSV Export**: Outputs the combined events into a single CSV file, allowing users to easily save and analyze the events they've discovered. This feature is particularly useful for users who may want to perform further analysis or keep a record of events.

## Prerequisites
- Python
- Pandas
- BeautifulSoup4
- Dotenv

## Installation
- pip install -r requirements.txt
  
## Usage 
- python main.py