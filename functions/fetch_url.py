import requests
from typing import Optional, Tuple

def fetch_url(working_directory: str, url: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Makes an HTTP GET request to the specified URL and returns the content 
    and status code. This tool is designed for AI agents to retrieve real-time data.

    Args:
        url (str): The full URL to fetch content from (e.g., "https://api.example.com/data").

    Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing 
                                              (content, error_message).
                                              If successful, content is the text 
                                              and error_message is None.
                                              If failed, content is None and 
                                              error_message contains the reason.
    """
    try:
        # Set a reasonable timeout to prevent the agent from hanging indefinitely
        response = requests.get(url, timeout=10)
        
        # Check for HTTP status codes indicating failure (4xx or 5xx)
        if response.status_code != 200:
            error_message = f"HTTP Error: Received status code {response.status_code} ({response.reason}). The URL might be incorrect, rate-limited, or inaccessible."
            return None, error_message

        # Attempt to decode the content as text
        content = response.text
        return content, None

    except requests.exceptions.Timeout:
        error_message = f"Connection Timeout: The request timed out after 10 seconds for URL {url}."
        return None, error_message
    except requests.exceptions.TooManyRedirects:
        error_message = "Redirection Error: Too many redirects were encountered while accessing the URL."
        return None, error_message
    except requests.exceptions.RequestException as e:
        # Catch all other request-related errors (DNS failure, connection refused, etc.)
        error_message = f"An unexpected network error occurred while connecting to {url}: {e}"
        return None, error_message
