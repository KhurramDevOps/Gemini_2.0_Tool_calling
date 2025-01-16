from langchain_core.tools import tool
import requests

@tool(parse_docstring=True)
def calculator(expression: str) -> float:
    """
    Evaluates a given mathematical expression.

    This function takes a mathematical expression as a string, evaluates it, and returns the result.
    It handles basic arithmetic, parentheses, and more complex mathematical calculations.

    Args:
        expression (str): A mathematical expression to evaluate, e.g., "3 + 5 * (2 - 8)".

    Returns:
        Union[float, str]: The result of the evaluated expression, or an error message if invalid.

    Example:
        >>> evaluate_expression("3 + 5 * 2")
        13.0
        >>> evaluate_expression("2 / 0")
        'Error: Division by zero.'
        >>> evaluate_expression("invalid + expression")
        'Error: Invalid input.'
    """
    try:
        # Use eval to compute the result securely
        result = eval(expression, {"__builtins__": None}, {})
        if isinstance(result, (int, float)):  # Ensure result is a number
            return result
        else:
            return "Error: Invalid mathematical expression."
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception:
        return "Error: Invalid input."
    
@tool(parse_docstring=True)
def latest_news(api_key: str = "c75303be293245a88968d6383fe4e32e", 
                country: str = None, category: str = None, query: str = None, limit: int = 5):
    """
    Fetch the latest news headlines using the NewsAPI.

    Args:
        api_key (str): Your NewsAPI key.
        country (str, optional): The country for news headlines (e.g., "us", "pk"). Default is None.
        category (str, optional): The category of news (e.g., "technology", "sports"). Default is None.
        query (str, optional): Keywords to search for specific news (e.g., "California fire"). Default is None.
        limit (int): Number of headlines to fetch (default is 5).

    Returns:
        list: A list of the latest news headlines or error messages.

    Example:
        >>> latest_news(api_key="your_api_key_here", country="us", category="technology", limit=3)
        ['Headline 1', 'Headline 2', 'Headline 3']
        >>> latest_news(api_key="your_api_key_here", query="California fire", limit=3)
        ['Headline 1', 'Headline 2', 'Headline 3']
    """
    # If no parameters are provided, switch to a default behavior
    if not (country or category or query):
        base_url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": api_key,
            "pageSize": limit,
            "sortBy": "publishedAt"  # Sort by the most recent articles
        }
    elif query:
        base_url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": api_key,
            "q": query,
            "pageSize": limit,
        }
    else:
        base_url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": api_key,
            "country": country,
            "category": category,
            "pageSize": limit,
        }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return [article["title"] for article in data.get("articles", [])]
    except requests.exceptions.RequestException as e:
        return [f"Error fetching news: {e}"]
    except KeyError:
        return ["Error: Unexpected response structure."]

    
@tool(parse_docstring=True)
def get_stock_price(symbol: str) -> str:
    """Fetches the current stock price of a company based on its stock symbol using the Polygon API.

    Args:
        symbol (str): The stock symbol of the company (e.g., 'AAPL' for Apple, 'GOOGL' for Google).

    Returns:
        str: A message containing the current stock price of the company.

    Raises:
        HTTPError: If the HTTP request to the stock API fails (e.g., 404 or 500 status).
        RequestException: If there is an issue with the request itself (e.g., connection error).
        Exception: For any other unexpected errors during the execution of the function.

    """
    api_key = "bgXWqWwosch5iZV76iQUagp8KkaINWka"  # Replace this with your actual secret API key from Polygon
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/prev"  # Polygon endpoint for previous close price

    try:
        # Send a GET request with the API key
        response = requests.get(url, params={'apiKey': api_key})
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)

        # Assuming the data contains 'close' in the response for the last closing price
        data = response.json()
        price = data.get('results', [{}])[0].get('c')  # 'c' is the closing price

        if price:
            return f"Tool used: get_stock_price\n get_stock_price tool is used to find The current price of {symbol} is ${price}"
        else:
            return f"Error: Could not retrieve stock data for {symbol}.\nTool used: get_stock_price"

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}\nTool used: get_stock_price"
    except requests.exceptions.RequestException as req_err:
        return f"Request error occurred: {req_err}\nTool used: get_stock_price"
    except Exception as err:
        return f"An unexpected error occurred: {err}\nTool used: get_stock_price"


@tool(parse_docstring=True)
def get_weather(city: str) -> str:
    """
    Fetches the current weather for a given city using the OpenWeatherMap API.

    Args:
        city (str): Name of the city to get weather for.

    Returns:
        str: Weather information or error message.
    """
    api_key = "32443eadd3962154515f22cfe08c11d6"
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        # Extract weather details
        city_name = data["name"]
        temp = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Format the result
        return (
            f"Weather in {city_name}:\n"
            f"Temperature: {temp}°C\n"
            f"Condition: {weather_description.capitalize()}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )

    except requests.exceptions.HTTPError:
        return "City not found. Please check the city name."
    except Exception as e:
        return f"An error occurred: {e}"

from googlesearch import search
@tool(parse_docstring=True)
def google_search_tool(query: str, num_results: int = 5):
    """
    Perform a Google search for a given query and return the top results.

    Args:
        query (str): The search query.
        num_results (int): Number of search results to return. Default is 5.

    Returns:
        list: A list of URLs for the top search results.
    """
    try:
        # Perform the search
        results = search(query, num_results=num_results)
        return list(results)
    except Exception as e:
        return f"An error occurred during the search: {e}"
    
@tool(parse_docstring=True)
def get_distance(location1: str, location2: str) -> str:
    """
    Calculates the distance between two locations using the OpenCage Geocoder API.

    This function uses the OpenCage Geocoder API to get the geographic coordinates (latitude and longitude)
    of the provided locations, then computes the distance between the two points using the Haversine formula.

    Args:
        location1 (str): The first location (e.g., "New York").
        location2 (str): The second location (e.g., "Los Angeles").

    Returns:
        str: A message containing the calculated distance in kilometers between the two locations.

    Raises:
        Exception: If either location is invalid or the API requests fail.
    """

    api_key = "289a5737aafd44809b61ef6667394dc5"  # Replace with your OpenCage API key

    # Geocode the origin location
    url1 = f"https://api.opencagedata.com/geocode/v1/json?q={location1}&key={api_key}"
    response1 = requests.get(url1)

    # Geocode the destination location
    url2 = f"https://api.opencagedata.com/geocode/v1/json?q={location2}&key={api_key}"
    response2 = requests.get(url2)

    # Check if both responses are successful
    if response1.status_code == 200 and response2.status_code == 200:
        data1 = response1.json()
        data2 = response2.json()

        # Extract latitude and longitude for both locations
        lat1, lon1 = data1['results'][0]['geometry']['lat'], data1['results'][0]['geometry']['lng']
        lat2, lon2 = data2['results'][0]['geometry']['lat'], data2['results'][0]['geometry']['lng']

        # Calculate the distance using the Haversine formula
        from math import radians, sin, cos, sqrt, atan2

        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Radius of the Earth in kilometers
        radius = 6371.0

        # Calculate the distance
        distance = radius * c

        return f"Tool used: get_distance\n get_distance tool is used to find The distance between {location1} and {location2} is {distance:.2f} km."

    else:
        return f"Error: Could not calculate the distance. Check if both locations are valid.\nTool used: get_distance"