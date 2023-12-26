import asyncio
import websockets
from requests import Session

session = Session()


async def hello(websocket, path):
    # Send a hello message immediately upon connection
    await websocket.send("Connected! Server says: Hello!")

    try:
        # Send "hello" message every 2 seconds until the connection is closed
        while True:
            await asyncio.sleep(2)
            await websocket.send("Hello from the server!")

    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed from client.")

start_server = websockets.serve(hello, "localhost", 8201)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
