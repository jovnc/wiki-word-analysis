# Wiki Word Analysis
#### By: Jovan Ng Chengen, Singapore (2023)
#### Description:

This is a Flask Web Application that prompts users for a search term in wikipedia, then scrapes through the wikipedia page for all words in the content page, and then displays the top 5 words in the page, along with their frequency as well as their percentage of occurrence. It also utilises `Wordcloud` Python Library to generate a wordcloud SVG and displays it for users to get a visualisation of the distribution of all the words in the wikipedia page. All content is generated dynamically, and the application performs in real time web scraping of the wikipedia page using `BeautifulSoup4` Python Library.

---

### Future Updates:
1. Integration with AI tools such as OpenAI to summarise the wikipedia page into bite-sized information

2. More Data Visualisation Tools

---

### How to use the Bot
1. Create a Python virtual environment using `venv`
2. Install dependencies on the virtual environemnt using `pip install -r requirements.txt`
3. Start the app using `flask run`
