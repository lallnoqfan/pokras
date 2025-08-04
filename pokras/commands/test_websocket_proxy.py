from asyncio import TimeoutError
from sys import stderr

from websockets import connect, WebSocketException

from config import ConnectionConfig


async def test_websocket_proxy():
    wss_server_url = "wss://echo.websocket.events"
    proxy_url = ConnectionConfig.PROXY_URL

    print(f"Attempting to connect to WebSocket server through proxy {proxy_url}...")
    try:
        # websockets library uses aiohttp for proxy support
        # The syntax is slightly different but achieves the same result
        async with connect(wss_server_url, proxy=proxy_url, open_timeout=10) as websocket:

            print("Successfully connected to WebSocket server!")

            # Send a simple message to confirm communication
            await websocket.send("Hello, WebSocket!")

            # Await a response from the server
            response = await websocket.recv()
            print(f"Received message from server: {response}")

    except WebSocketException as e:
        print(f"WebSocket error occurred: {e}", file=stderr)
        print("This often indicates that the proxy cannot handle WebSocket traffic.", file=stderr)
    except TimeoutError:
        print("Timeout occurred. Could not establish WebSocket connection.", file=stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=stderr)
