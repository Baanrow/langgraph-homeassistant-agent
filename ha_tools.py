from langchain_core.tools import tool
from config import HA_TOKEN, HA_URL_LOCAL
import requests
from typing import Annotated

@tool
def get_light_state(entity_id: Annotated[str, "The unique ID of the light."]) -> dict:
    """
    Gets the on/off state of the light in Home Assistant.
    Always use the "light." prefix, e.g. "light.kitchen_1".

    Args:
        entity_id: The unique ID of the light.

    Returns:
        dict: A dict containing the current state of the light,
        e.g. {"state": "on"}
    """
    try:
        url = f"{HA_URL_LOCAL}/{entity_id}"
        headers = {
            "Authorization": f"Bearer {HA_TOKEN}",
            "Application-Type": "content/json"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        state = data.get("state")
        return {"state": state}
    except requests.RequestException as e:
        return {"error": "Unable to get light state"}

tools = [get_light_state]
