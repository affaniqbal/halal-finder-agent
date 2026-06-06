import os
import googlemaps

def get_google_maps_client():
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_PLACES_API_KEY not set in .env")
    return googlemaps.Client(key=api_key)


def search_restaurants(query: str, location: str = "London") -> list[dict]:
    """Search for restaurants using Google Places API."""
    gmaps = get_google_maps_client()
    full_query = f"{query} restaurant {location}"
    results = gmaps.places(query=full_query)

    restaurants = []
    for place in results.get("results", [])[:5]:
        restaurant = {
            "name": place.get("name"),
            "address": place.get("formatted_address"),
            "rating": place.get("rating"),
            "user_ratings_total": place.get("user_ratings_total"),
            "place_id": place.get("place_id"),
            "maps_link": f"https://www.google.com/maps/place/?q=place_id:{place.get('place_id')}",
        }
        restaurants.append(restaurant)

    return restaurants


def get_place_details(place_id: str) -> dict:
    """Get detailed info about a place including reviews that may mention halal."""
    gmaps = get_google_maps_client()
    result = gmaps.place(
        place_id=place_id,
        fields=["name", "formatted_address", "rating", "review", "website", "formatted_phone_number", "editorial_summary"]
    )
    place = result.get("result", {})

    reviews = place.get("reviews", [])
    review_texts = [r.get("text", "") for r in reviews]

    halal_mentions = [r for r in review_texts if "halal" in r.lower()]

    return {
        "name": place.get("name"),
        "address": place.get("formatted_address"),
        "rating": place.get("rating"),
        "website": place.get("website"),
        "phone": place.get("formatted_phone_number"),
        "editorial_summary": place.get("editorial_summary", {}).get("overview"),
        "halal_mentions_in_reviews": halal_mentions,
        "maps_link": f"https://www.google.com/maps/place/?q=place_id:{place_id}",
    }


# Tool definitions for the Anthropic API
TOOL_DEFINITIONS = [
    {
        "name": "search_restaurants",
        "description": "Search for restaurants near a location using Google Places. Use this first to find candidate restaurants.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query e.g. 'halal Turkish' or 'halal Lebanese'"
                },
                "location": {
                    "type": "string",
                    "description": "Location to search near e.g. 'Shoreditch London' or 'Bethnal Green London'"
                }
            },
            "required": ["query", "location"]
        }
    },
    {
        "name": "get_place_details",
        "description": "Get detailed information about a specific restaurant including reviews that may mention halal status. Use this after search_restaurants to verify halal claims.",
        "input_schema": {
            "type": "object",
            "properties": {
                "place_id": {
                    "type": "string",
                    "description": "The Google Places place_id from search_restaurants results"
                }
            },
            "required": ["place_id"]
        }
    }
]


def run_tool(tool_name: str, tool_input: dict) -> str:
    """Execute a tool by name and return result as string."""
    if tool_name == "search_restaurants":
        results = search_restaurants(**tool_input)
        return str(results)
    elif tool_name == "get_place_details":
        result = get_place_details(**tool_input)
        return str(result)
    else:
        return f"Unknown tool: {tool_name}"
