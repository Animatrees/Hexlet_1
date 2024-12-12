import asyncio

from controller import initialize


async def main():
    await initialize()


if __name__ == '__main__':
    asyncio.run(main())
