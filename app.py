from flask import Flask, render_template, redirect, request, Markup
from script import scrape_link, add_percentage, reduce_df_memory, create_wordcloud

# Initialise Flask Object
app = Flask(__name__)


# Default root route
@app.route("/")
def main():
    return render_template("index.html", name = "Jovan")


# Search for wikipedia page and display results
@app.route("/search", methods = ["POST", "GET"])
def search():
    if request.method == "POST":
        search_term = request.form.get("search")
        # Scrape the link and store it as a pandas df
        df = scrape_link(search_term)
        
        # Add percentage column
        df = add_percentage(df)
    
        # Reducing memory usage of df by changing datatypes
        df = reduce_df_memory(df)
        
        tables = [df.head(5).to_html(classes='data')]
        
        # import svg
        create_wordcloud()
        svg = open('results.svg').read()
        
        return render_template("results.html", tables = tables, results = Markup(svg))
    else:
        return redirect("/")