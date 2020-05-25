import os
import time
import random
import json
import asyncio
import websockets


class Server():     
    async def manageRequests(self, websocket, path):
        async for message in websocket:
            print(message)

if __name__ == "__main__":
    server = Server()
    print("Starting Mahjong Server...")
    asyncio.get_event_loop().run_until_complete(websockets.serve(server.manageRequests, "localhost", 8081))
    asyncio.get_event_loop().run_forever()
