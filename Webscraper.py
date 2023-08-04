import csv
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

# Function to extract star rating number from a row
def extract_star_rating(row):
    try:
        # Get the class attribute value and check if "star" and "fill" are present
        class_attribute = row.get('class')
        if class_attribute and "star" in class_attribute and "fill" in class_attribute:
            return row.text.strip()
        else:
            return 'Not Found'
    except:
        return 'Not Found'

def extract_country(text):
    try:
        country = text.split('(')[-1].split(')')[0].strip()
        return country
    except:
        return 'Not Found'


# Function to extract value from the table row
def get_value(div_element, row_label):
    try:
        row = div_element.find('td', text=row_label)
        if row:
            value = row.find_next('td').text.strip()
            return value
        else:
            return 'Not Found'
    except:
        return 'Not Found'

def get_verification(trip):

    try:
       trip_verified = trip[0].strip()
       Verified = trip_verified.replace("✅", "").strip() if trip_verified else 'Not Found'
       return Verified
    except:
       return "Not Found"

def scrape_review_page(driver, url):
    driver.get(url)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    div_elements = soup.find_all('div', class_='body')

    review_data = []
    for div_element in div_elements:
        data_dict = {
            'Title': div_element.find('h2', class_='text_header').text.strip(),
            'Reviewer': div_element.find('span', itemprop='name').text.strip(),
            'Country': extract_country(div_element.find('h3', class_='text_sub_header userStatusWrapper').text),
            'Date Published': div_element.find('time', itemprop='datePublished').text.strip(),
            'Trip Verified': get_verification(div_element.find('div', class_='text_content').text.split("|"))
        }

        # Check for Verified status
        try:
            trip = div_element.find('div', class_='text_content').text.split("|")
            trip_verified = trip[0].strip()
            data_dict['Verified'] = trip_verified.replace("✅", "").strip() if trip_verified else 'Not Found'
        except:
            data_dict['Verified'] = 'Not Found'

        # Get star ratings for each category from 1 to 10
        for i in range(1, 11):
            try:
                label_element = div_element.select_one(f'table tbody tr:nth-of-type({i}) td:nth-of-type(1)')
                if label_element:
                    label = label_element.text.strip()
                    value_elements = div_element.select(f'table tbody tr:nth-of-type({i}) td:nth-of-type(2) span[class*="star fill"]')
                    if value_elements:
                        # Get the last star rating (assuming the last one is the latest rating)
                        value = extract_star_rating(value_elements[-1])
                        data_dict[label] = value
                    else:
                        data_dict[label] = 'Not Found'
            except:
                pass

        # Get values for Aircraft, Type Of Traveller, Seat Type, Route, Date Flown
        try:
            data_dict['Aircraft'] = get_value(div_element, 'Aircraft')
            data_dict['Type Of Traveller'] = get_value(div_element, 'Type Of Traveller')
            data_dict['Seat Type'] = get_value(div_element, 'Seat Type')
            data_dict['Route'] = get_value(div_element, 'Route')
            data_dict['Date Flown'] = get_value(div_element, 'Date Flown')
            data_dict['Recommended'] = get_value(div_element, "Recommended")
        except:
            pass

        # Get Review Body
        try:
            main_review = trip[1].strip()
            data_dict['Review'] = main_review if main_review else 'NA'
        except:
            data_dict['Review'] = 'NA'

        review_data.append(data_dict)

    return review_data


if __name__ == "__main__":
    # Path to the downloaded web driver executable
    driver_path = '/path/to/chromedriver'  # Replace this with the actual path to the downloaded driver

    # Base URL for the reviews
    base_url = "https://www.airlinequality.com/airline-reviews/british-airways/page/"

    # List to store all review data
    all_review_data = []

    # Start from page 1
    page_number = 1

    # Initialize the Chrome web driver
    driver = webdriver.Chrome(executable_path=driver_path)

    while True:
        url = base_url + str(page_number) + "/"
        review_data = scrape_review_page(driver, url)

        # If no review elements found, break the loop as it means we reached the last page
        if not review_data:
            break

        all_review_data.extend(review_data)

        # Move to the next page
        page_number += 1

    # Close the web driver
    driver.quit()

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(all_review_data)

    # Reorder the columns with "Review" as the last column
    cols = df.columns.tolist()
    cols.remove('Review')
    cols.append('Review')
    df = df[cols]

    # Save the DataFrame to a CSV file
    df.to_csv('reviews_data_all_pages.csv', index=False)

    # # Print the DataFrame (optional)
    # print(df)
