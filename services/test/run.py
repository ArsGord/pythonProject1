import asyncio

from services.test import TestHandler

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    handler = TestHandler()
    loop.create_task(handler.receive_messages())

    # we enter a never-ending loop that waits for data
    # and runs callbacks whenever necessary.
    print('[x] Awaiting RPC requests')
    loop.run_forever()
