import os
import json
import subprocess
import PyPDF2
import pandas as pd
import requests
from datetime import datetime
try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None

def get_tavily_client():
    api_key = os.getenv("TAVILY_API_KEY")
    if TavilyClient and api_key and api_key != "tvly-dev-dummy":
        return TavilyClient(api_key=api_key)
    return None

def web_search(query: str) -> str:
    """Performs a web search to get real-time answers and news. Uses Tavily (Primary) or Google (Fallback)."""
    client = get_tavily_client()
    
    # Attempt Primary Search (Tavily)
    if client:
        try:
            response = client.search(query=query, search_depth="basic", max_results=3)
            results = response.get("results", [])
            if results:
                return "\n".join([f"Title: {r.get('title')}\nURL: {r.get('url')}\nContent: {r.get('content')}\n" for r in results])
        except Exception:
            pass # Fall through to fallback
            
    # Attempt Fallback Search (GoogleSearch-Python - No Key Required)
    try:
        from googlesearch import search
        results = list(search(query, num_results=3))
        if results:
            formatted = f"Fallback Search Results for '{query}':\n"
            for i, url in enumerate(results, 1):
                formatted += f"{i}. {url}\n"
            return formatted + "\n*(Note: Used fallback search engine. For richer news summaries, please add TAVILY_API_KEY to .env.)*"
    except Exception as e:
        return f"Web Search Error (All providers failed): {str(e)}\n\nPlease ensure you have a valid TAVILY_API_KEY in your .env file for reliable real-time news."
    
    return "No web search results found. Please check your internet connection or API keys."

def read_file(file_path: str) -> str:
    """Reads the contents of a PDF or CSV file."""
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    ext = file_path.lower().split(".")[-1]
    
    try:
        if ext == "pdf":
            text = ""
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                # Limit to 5 pages to avoid massive token usage
                for i in range(min(5, len(reader.pages))):
                    page = reader.pages[i]
                    text += page.extract_text() + "\n"
            return text
        elif ext == "csv":
            df = pd.read_csv(file_path)
            # Return first 50 rows as string
            return df.head(50).to_string()
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read(2000)
    except Exception as e:
        return f"File Read Error: {str(e)}"

def calculate(expression: str) -> str:
    """Evaluates a mathematical expression."""
    allowed_chars = "0123456789+-*/(). "
    if any(c not in allowed_chars for c in expression):
        return "Error: Invalid characters in mathematical expression. Only use digits and +-*/()."
    
    try:
        # eval is generally dangerous, but we restricted characters heavily above
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Calculation Error: {str(e)}"

def schedule_event(event: str, time: str) -> str:
    """Schedules an event by writing it to a JSON file."""
    schedule_file = "schedule.json"
    
    try:
        if os.path.exists(schedule_file):
            with open(schedule_file, "r") as f:
                data = json.load(f)
        else:
            data = []
            
        data.append({
            "event": event,
            "time": time,
            "scheduled_at": datetime.now().isoformat()
        })
        
        with open(schedule_file, "w") as f:
            json.dump(data, f, indent=4)
            
        return f"Successfully scheduled '{event}' for {time}."
    except Exception as e:
        return f"Scheduler Error: {str(e)}"

def execute_code(code: str) -> str:
    """Executes arbitrary python code. Use with caution."""
    # Write code to a temporary file
    script_path = "temp_executor.py"
    try:
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)
            
        # Run the code safely with a timeout
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            timeout=10  # 10 seconds timeout
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\nErrors:\n{result.stderr}"
            
        return output if output else "Code executed successfully with no output."
    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out (max 10 seconds)."
    except Exception as e:
        return f"Code Execution Error: {str(e)}"
    finally:
        # Cleanup
        if os.path.exists(script_path):
            os.remove(script_path)

def get_weather(location: str) -> str:
    """Gets the current weather and temperature for a given location using a free API."""
    try:
        url = f"https://wttr.in/{location.replace(' ', '+')}?format=j1"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            temp_c = current['temp_C']
            desc = current['weatherDesc'][0]['value']
            humidity = current['humidity']
            wind = current['windspeedKmph']
            
            return f"The current weather in {location} is {desc}. Temperature is {temp_c}°C. Humidity: {humidity}%, Wind: {wind} km/h."
        else:
            # Fallback to plain text if JSON fails
            text_resp = requests.get(f"https://wttr.in/{location.replace(' ', '+')}?format=3", timeout=10)
            if text_resp.status_code == 200:
                return f"Current weather for {location}: {text_resp.text.strip()}"
            return f"Weather lookup failed for {location} (API returned {response.status_code})"
    except Exception as e:
        return f"Weather lookup error: {str(e)}"

# Map for tool calling
TOOLS_MAP = {
    "web_search": web_search,
    "read_file": read_file,
    "calculate": calculate,
    "schedule_event": schedule_event,
    "execute_code": execute_code,
    "get_weather": get_weather
}

# JSON Schema for Groq
GROQ_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current temperature, weather conditions, and forecast for a specific city or location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name, e.g., 'Jaipur' or 'New York'."
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Perform a real-time web search for current events, news, or general information not in your training data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of local PDF or CSV files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The absolute or relative path to the file to extract data from."
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression. Only standard operators allow (+-*/()).",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate, like '2 * (3 + 4)'."
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule_event",
            "description": "Schedule a meeting, appointment, or reminder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event": {
                        "type": "string",
                        "description": "The name or description of the event."
                    },
                    "time": {
                        "type": "string",
                        "description": "The time the event is scheduled for."
                    }
                },
                "required": ["event", "time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_code",
            "description": "Run Python code locally on the machine. You can use this for advanced calculations or scripts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The python code to execute. Standard output will be returned."
                    }
                },
                "required": ["code"]
            }
        }
    }
]
