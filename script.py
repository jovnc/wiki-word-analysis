# Import relevant third party libraries
from bs4 import BeautifulSoup
import pandas as pd
import requests
import enchant
import re
import sys
from wordcloud import WordCloud


# Initialising objects
enchantObj = enchant.Dict("en_US")


# Keep track of scraped links
scraped_links = []

# Initialise dictionary of all words
dictionary = dict()


# Scraping Wikipedia to find all the urls for the table of content and store the data into a pandas DF to be returned
def scrape_link(search_term):
    
    # Input cleaning
    search_term = str(search_term)
    search_term = search_term.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{search_term}"

    # Get BS Object from the url for web scraping
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")

    # Check if the website is a valid website
    invalid = soup.find("div", class_="no-article-text-sister-projects")
    if invalid:
        sys.exit(
            "There is currently no wikipedia site for your search term, please try again."
        )

    print(f"Scraping {url} for data...")

    # Scrape data from each page: extract all text and add them into a hash map
    scrape_data_from_page(url)
    
    # Creating a pandas dataframe to access the data
    df = create_df(dictionary)

    
    return df
        

# Creating pandas dataframe
def create_df(dictionary):
    df = pd.DataFrame(list(dictionary.items()), columns = ["word", "count"])
    df = df.sort_values("count", ascending = False)
    df = df.reset_index(drop=True)

    return df



# Function to scrape all the text inside the linked page
def scrape_data_from_page(href):
    response = requests.get(href)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all the visible text on the page
    div_class = soup.find('div', class_= 'mw-body-content')
    # Extract text from <p> tags
    p_texts = [p.get_text() for p in div_class.find_all('p')]
    p_texts = [p.split() for p in p_texts]
    p_texts = [item for sublist in p_texts for item in sublist]

    words = p_texts

    for word in words:
        # Cleaning of data: removal of all other unwanted characters
        word = re.search("[a-zA-Z\-]+", word)
        if word:
            word = word.group()

            # Check if the word is a valid word in the dictionary
            if enchantObj.check(word):
                word = word.lower()
                # Add word into dictionary count
                if word not in dictionary.keys():
                    dictionary[word] = 1
                else:
                    dictionary[word] += 1


# Finding top 3 most commonly used words
def most_common_words(df):
    dict = df.head(3).to_dict()
    
    print("\nThe top three words are: ")
    for i, key in enumerate(dict['count']):
        print(f"{i+1}. {dict['word'][key]}: {dict['count'][key]} words ({dict['percentage'][key]})")
        
        
    sum = df["count"].sum()
    print(f"There is a total of {sum} words\n")
        
# Store data collected into a CSV
def store_to_csv(df):
    print("Creating CSV File...")
    df.to_csv("results.csv", sep="\t")
    print("Successfully created results.csv file!")
    

# Store data collected into JSON
def store_to_json(df):
    print("Creating JSON File...")
    df.to_json("results.json")
    print("Successfully created results.json file!")


# Create new percentage column
def add_percentage(df):
    sum = df["count"].sum()
    percent =[]
    
    for i in range(len(df)):
        percentage = df["count"][i]/sum
        percent.append(f"{round(percentage, 4)}")
        
    df["percentage"] = percent
    
    return df  
    

# Changing data types of dataframe columns for more efficient memory usage
def reduce_df_memory(df):
    df['word'] = df['word'].astype("str")
    df['count'] = df['count'].astype("int16")
    df['percentage'] = df['percentage'].astype("float")
    return df

  
# Generate word cloud 
def create_wordcloud():
    wordcloud = WordCloud(max_words=50, background_color="white").generate_from_frequencies(dictionary)
    svg = wordcloud.to_svg()
    with open("results.svg", "w") as f:
        f.write(svg)


# Main function to run the entire program
def main():
    # Set the url for the website that we are scraping and send GET request for the website
    search_term = input("What wikipedia site would you like so search?\nSearch: ")
    
    # Scrape the link and store it as a pandas df
    df = scrape_link(search_term)
    
    # Add percentage column
    df = add_percentage(df)
    
    # Reducing memory usage of df by changing datatypes
    df = reduce_df_memory(df)
  
    # Search for top 3 most common words in the DF
    most_common_words(df)
    
    # Storing of data into CSV and JSON after data manipulation and cleaning for presentation
    store_to_json(df)
    store_to_csv(df)
    


if __name__ == "__main__":
    main()
