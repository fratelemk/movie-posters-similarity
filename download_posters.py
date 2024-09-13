import os
import pickle
import asyncio
import aiohttp
import aiofiles
from tqdm.asyncio import tqdm


async def _get(session, poster):
    try:
        async with session.get(poster[1]) as response:
            data = await response.read()
            async with aiofiles.open(poster[0], 'wb') as f:
                await f.write(data)
    except Exception as e:
        print(f"An error occurred while downloading {poster[1]}: {e}")


async def download(posters):
    async with aiohttp.ClientSession() as session:
        tasks = [_get(session, poster) for poster in posters]
        await tqdm.gather(*tasks, desc=f'Downloading posters', total=len(posters))


def main():
    with open('input/posters.pkl', 'rb') as file:
        posters = pickle.load(file)

    asyncio.run(download(posters))


if __name__ == '__main__':
    main()