from asyncio import TimeoutError, run
from sys import stderr

from aiohttp import ClientSession, ClientError

from config import ConnectionConfig


async def test_http_proxy() -> None:
    """
    Проверка http соединения через прокси.
    Йеп, ai generated.
    """
    test_url = "https://api.sampleapis.com/coffee/hot"
    proxy_url = ConnectionConfig.PROXY_URL

    print(f"Attempting to connect to {test_url} through proxy {proxy_url}...")
    try:
        async with ClientSession() as session:
            # The 'proxy' parameter is what aiohttp uses to route traffic
            async with session.get(test_url, proxy=proxy_url, timeout=10) as resp:
                # This will print the HTTP status code (e.g., 200 for success)
                print(f"Connection successful! HTTP Status Code: {resp.status}")
                # Print the response to confirm it's working
                response_data = await resp.json()
                print("Response data from httpbin.org:")
                print(response_data)

    except ClientError as e:
        print(f"aiohttp ClientError occurred: {e}", file=stderr)
        print("This typically means the proxy server is not running or the proxy URL is incorrect.", file=stderr)
    except TimeoutError:
        print("Timeout occurred. Could not connect to the proxy within 10 seconds.", file=stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=stderr)


if __name__ == '__main__':
    run(test_http_proxy())
