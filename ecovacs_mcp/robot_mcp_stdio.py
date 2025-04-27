import os
import sys
import httpx
from pydantic import Field

from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP("RobotControl")

# API configuration
API_KEY = os.getenv('ECO_API_KEY')  
API_URL = "https://open.ecovacs.cn"



ENDPOINT_ROBOT_CTL = "robot/ctl"
ENDPOINT_ROBOT_DEVICE_LIST = "robot/deviceList"
REQUEST_TIMEOUT = 10.0  # Set request timeout (seconds)

async def call_api(endpoint: str, params: dict, method: str = 'post') -> dict:
    """
    General API call function
    
    Args:
        endpoint: API endpoint
        params: Request parameters
        method: Request method, 'get' or 'post'
    
    Returns:
        Dict: API response result, format {"msg": "OK", "code": 0, "data": [...]}
    """
    # Build complete URL
    url = f"{API_URL}/{endpoint}"
    
    # Ensure all parameters are strings
    params = {k: str(v) for k, v in params.items()}
    
    # Add API key
    if API_KEY:
        params.update({"ak": API_KEY})
    
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Content-Type": "application/json"}
            if method.lower() == 'get':
                response = await client.get(url, params=params, timeout=REQUEST_TIMEOUT)
            else:
                response = await client.post(url, json=params, headers=headers, timeout=REQUEST_TIMEOUT)
            
            response.raise_for_status()
            return response.json()
    
    except Exception as e:
        # Return unified error format when an error occurs
        return {"msg": f"Request failed: {str(e)}", "code": -1, "data": []}

@mcp.tool()
async def set_cleaning(
    nickname: str = Field(description="Robot nickname, supports fuzzy matching", default=""),
    act: str = Field(description="Cleaning action, s-start cleaning, r-resume cleaning, p-pause cleaning, h-stop cleaning", default="s")
) -> dict:
    """
    Start robot cleaning
    
    Args:
        nickname: Robot nickname, used to find device
        act: Cleaning action s-start cleaning, r-resume cleaning, p-pause cleaning, h-stop cleaning
    Returns:
        Dict: Dictionary containing execution results
    """
    return await call_api(ENDPOINT_ROBOT_CTL, {"nickName": nickname, "cmd": "Clean", "act": act})

@mcp.tool()
async def set_charging(
    nickname: str = Field(description="Robot nickname, used to find device"),
    act: str = Field(description="Robot action, go-start begin returning to charging station, stopGo stop returning to charging station", default="go-start")
) -> dict:
    """
    Make robot return to charging station
    
    Args:
        nickname: Robot nickname, used to find device
        act: Robot action, go-start begin returning to charging station, stopGo stop returning to charging station
    
    Returns:
        Dict: Dictionary containing execution results
    """
    return await call_api(ENDPOINT_ROBOT_CTL, {"nickName": nickname, "cmd": "Charge", "act": act})

@mcp.tool()
async def get_work_state(
    nickname: str = Field(description="Robot nickname, used to find device")
) -> dict:
    """
    Query robot working status
    
    Args:
        nickname: Robot nickname, used to find device
    
    Returns:
        Dict: Dictionary containing robot working status
    """
    return await call_api(ENDPOINT_ROBOT_CTL, {"nickName": nickname, "cmd": "GetWorkState", "act": ""})

@mcp.tool()
async def get_device_list() -> dict:
    """
    Query robot list

    Returns:
        Dict: Dictionary containing list of robot nicknames
    """
    return await call_api(ENDPOINT_ROBOT_DEVICE_LIST, {}, method='get')

def main():
    """
    Main function, run MCP server in stdio mode
    """
    # Print startup information
    print("\n===== Starting MCP Robot Control Server (stdio mode) =====", file=sys.stderr)
    # Run MCP server in stdio mode
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()