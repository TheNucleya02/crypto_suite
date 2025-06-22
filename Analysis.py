from exa_py import Exa
import requests
import pandas as pd
import time
from crewai.tools import tool
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt

# IMPORT API KEYS
from dotenv import load_dotenv
import os

load_dotenv()
EXA = os.getenv("EXA_API")
GEMINI = os.getenv("GEMINI_API")
ALPHA=os.getenv("ALPHA_API")



exa = Exa(EXA)


"""News tool"""

@tool("search_tool")
def search_tool(symbol: str) -> str:
    """Search for the latest news and provide a summary about a given query using Exa."""
    # Perform the search and fetch the results
    result = exa.search_and_contents(symbol, summary=True)

    # Ensure results exist before processing
    if result.results:
        news_list = []
        for item in result.results:
            # Extracting attributes directly from the Result object
            news_item = {
                "title": item.title if hasattr(item, "title") else "No Title",
                "url": item.url if hasattr(item, "url") else "#",  # URL and ID are the same
                "id": item.id if hasattr(item, "id") else "#",  # ID is same as URL
                "score": item.score if hasattr(item, "score") else "No Score",
                "published_date": item.published_date if hasattr(item, "published_date") else "Unknown Date",
                "author": item.author if hasattr(item, "author") else "Unknown Author",
                "image": item.image if hasattr(item, "image") else "No Image",
                "favicon": item.favicon if hasattr(item, "favicon") else "No Favicon",
                "summary": item.summary if hasattr(item, "summary") else "No Summary",
                
            }
            news_list.append(news_item)

        # Format the news items into a readable string
        output = []
        for news_item in news_list[:5]:
            output.append(f"Title: {news_item['title']}\nURL: {news_item['url']}\nSummary: {news_item['summary']}\n")

        return "\n".join(output)
    else:
        return "No results found."

"""Price tool"""

@tool("price_tool")

def price_tool(symbol: str) -> str:
    """Get daily closing price for a given cryptocurrency ticker symbol for the previous 60 days"""
    url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market=USD&apikey={ALPHA_API}"
    r = requests.get(url)
    data = r.json()
    price_data = data["Time Series (Digital Currency Daily)"]
    daily_closing_price = {
        date : price_info['4. close'] for (date, price_info) in price_data.items()
    }
    df = pd.DataFrame.from_dict(daily_closing_price, orient="index", columns=["price"])
    df.index = pd.to_datetime(df.index)
    df["price"] = pd.to_numeric(df["price"])
    text_output = [
        f"{date.strftime('%Y-%m-%d')} - {row['price']:.2f}"
        for date, row in df.head(30).iterrows()
    ]
    return "\n".join(text_output)

"""# LLM - Gemini 2.0 flash"""

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
    api_key=GEMINI
)


news_analyst = Agent(
    role="Cryptocurrency News Analyst",
    goal="""Get news for a given cryptocurrency. Write 1 paragraph analysis of
    the market and make prediction - up, down or neutral.""",
    backstory="""You're an expert analyst of trends based on cryptocurrency news.
    You have a complete understanding of macroeconomic factors, but you specialize
    into analyzing news.
    """,
    verbose=True,
    allow_delegation=False,
    llm=llm,
    max_iter=5,
    memory=True,
    respect_context_window=True,
    inject_date=True,
    tools=[search_tool],
)

price_analyst = Agent(
    role="Cryptocurrency Price Analyst",
    goal="""Get historical prices for a User given cryptocurrency. Write 1 paragraph analysis of
    the market and make prediction - up, down or neutral.""",
    backstory="""You're an expert analyst of trends based on cryptocurrency
    historical prices. You have a complete understanding of macroeconomic factors,
    but you specialize into technical analys based on historical prices.
    """,
    verbose=True,
    allow_delegation=False,
    llm=llm,
    max_iter=5,
    memory=True,
    inject_date=True,
    respect_context_window=True,
    tools=[price_tool],
)

writer = Agent(
    role="Cryptocurrency Report Writer",
    goal="""Write 1 paragraph report of the Specific cryptocurrency market Provided by User.""",
    backstory="""
    You're widely accepted as the best cryptocurrency analyst that
    understands the market and have tracked every asset for more than 10 years. Your trends
    analysis are always extremely accurate.

    You're also master level analyst in the traditional markets and have deep understanding
    of human psychology. You understand macro factors and combine those multiple
    theories - e.g. cycle theory. You're able to hold multiple opininons when analysing anything.

    You understand news and historical prices, but you look at those with a
    healthy dose of skepticism. You also consider the source of news articles.

    Your most well developed talent is providing clear and concise summarization
    that explains very complex market topics in simple to understand terms.

    Some of your writing techniques include:

    - Creating a bullet list (executive summary) of the most importannt points
    - Distill complex analyses to their most important parts

    You writing transforms even dry and most technical texts into
    a pleasant and interesting read.""",
    llm=llm,
    verbose=True,
    max_iter=5,
    memory=True,
    inject_date=True,
    allow_delegation=False,
)

def final_summary(symbol: str) -> str:

    get_news_analysis = Task(
        description=f"""
        Use the search tool to get news for the {symbol} cryptocurrency

        The current date is {datetime.now()}.

        Compose the results into a helpful report""",
        expected_output="""Create 1 paragraph report for the cryptocurrency,
        along with a prediction for the future trend
        """,
        agent=news_analyst,

    )

    get_price_analysis = Task(
        description=f"""
        Use the price tool to get historical prices of {symbol} cryptocurrency

        The current date is {datetime.now()}.

        Compose the results into a helpful report""",
        expected_output="""Create 1 paragraph summary for the cryptocurrency,
        along with a prediction for the future trend
        """,
        agent=price_analyst,
    )

    write_report = Task(
        description=f"""Use the reports from the news analyst and the price analyst to
        create a report that summarizes the cryptocurrency""",
        expected_output="""1 paragraph report that summarizes the market and
        predicts the future prices (trend) for the cryptocurrency""",
        agent=writer,
        context=[get_news_analysis, get_price_analysis],
    )

    crew = Crew(
        agents=[news_analyst, price_analyst, writer],
        tasks=[get_news_analysis, get_price_analysis, write_report],
        verbose=False,
        process=Process.sequential,
        share_crew=False,
        max_rpm=15,
        function_calling_llm=llm,
        step_callback=lambda x: time.sleep(5)
    )

    results = crew.kickoff()
    return str(results)

def plot_market_graph(symbol):
    try:
        data = yf.download(symbol, period="7d", interval="1h", auto_adjust=True)  # Last 7 days hourly
        if data.empty:
            return None, f"❌ No data found for {symbol}"

        plt.figure(figsize=(10, 5))
        plt.plot(data['Close'], label=f"{symbol.upper()} Price", color='skyblue')
        plt.title(f"{symbol.upper()} - Market Price (7d)")
        plt.xlabel("Date")
        plt.ylabel("Price in USD")
        plt.legend()
        plt.grid(True)

        img_path = f"{symbol}_chart.png"
        plt.savefig(img_path)
        plt.close()
        return img_path, None
    except Exception as e:
        return None, f"⚠️ Error generating chart: {e}"
