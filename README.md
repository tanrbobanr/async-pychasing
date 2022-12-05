An asynchronous version of [pychasing](https://pypi.org/project/pychasing/) (a wrapper for the https://ballchasing.com API).
# Install
`pip install async-pychasing`
# Usage
This asynchronous wrapper functions similarly to `pychasing`; it is recommended that you [read the documentation](https://github.com/tanrbobanr/pychasing/blob/main/README.md) as it explains the core functionality. Additionally, all helper enumerations and types are used from the `pychasing` module, and are not included with `async-pychasing`. There are two main changes in the way this version should be used. Creating a `Client` is the same (although `async_pychasing` is used instead of `pychasing`):
```py
import async_pychasing
import pychasing

pychasing_client = async_pychasing.Client(
    token="your_token",
    auto_rate_limit=True,
    patreon_tier=pychasing.PatreonTier.none
)
```
but the way you interact with the client is slightly different; instead of calling methods directly from the `Client` instance, an `aiohttp.ClientSession` instance must be passed into the `Client`, which will then return a `async_pychasing.Session` instance. This `Session` instance is then how you interact with the API, and contains all the usual methods (although asynchronous). For example:
```py
import aiohttp
import asyncio

# keep in mind that a new aiohttp.ClientSession is being created simply for illustration. In reality, you should NOT create a new aiohttp.ClientSession for each individual request.
async def main() -> None:
    async with aiohttp.ClientSession() as cs:
        async with pychasing_client(cs) as bs: # or pychasing_client.session(cs)
            await bs.get_replay(...)

if __name__ == "__main__":
    asyncio.run(main())
```
Because we're using `aiohttp` instead of `requests`, the way we download replays through the `download_replays` method is slightly different (we use `<response>.content.iter_chunked(...)` instead of `<response>.iter_content(...)`):
```py
async def download_replay(bs: async_pychasing.Session, replay_id: str) -> None:
    async with bs.download_replay(replay_id) as replay:
        with open("my_replay.replay", "wb") as outfile: # or using an async file manager
            async for chunk in replay.content.iter_chunks(4096):
                outfile.write(chunk)
```
# Notes on rate limiting
By default (if rate limiting is enabled) the methods are rate limited similarly to `pychasing`, in which one function call waits until the previous call has completed. For faster call speeds, this can be avoided by using the `concurrent` and `ca_deviation` options upon `Client` instantiation, although there are some drawbacks. The main drawback is that there is a posibility for getting rate-limited by the API, whereas with `concurrent=False` that is not the case. If `concurrent=True`, the methods will be rate limited without consideration for execution time of the HTTP[s] request. To help account for this time, you can set `ca_deviation` to a float; this will cause each function to take \<ca_deviation\> seconds longer before allowing the next function call to go through, which can allow for some extra leeway with request speed variation. To optimize speed, you should try to separate your API calls from your processing. For example (listing 10 replays, then getting the GUID of each replay):

```py
import async_pychasing
import pychasing
import aiohttp
import asyncio

client = async_pychasing.Client(...)

async def get_guids(guids: list[str],
                    responses: asyncio.Queue[aiohttp.ClientResponse],
                    break_after: int) -> None:
    for i in range(break_after):
        r = await responses.get()
        j = await r.json()
        guids.append(j["match_guid"])


# ONLY getting the replay and putting it into the queue
async def fetch_replay(bs: async_pychasing.Session, id: str,
                       responses: asyncio.Queue[aiohttp.ClientResponse]
                       ) -> None:
    res = await bs.get_replay(id)
    await responses.put(res)


async def main(guids: list[str],
               responses: asyncio.Queue[aiohttp.ClientResponse]) -> None:
    async with aiohttp.ClientSession() as client_session:
        async with client(client_session) as ballchasing_session:
            replay_list = await bs.list_replays(count=10)
            replay_list_json = await replay_list.json()
            replay_ids = [r["id"] for r in replay_list_json["list"]]

            loop = asyncio.get_event_loop()
            tasks: list[asyncio.Task] = []
            for id in replay_ids:
                tasks.append(loop.create_task(fetch_replay(ballchasing_session,
                                                           id,
                                                           responses)))
            tasks.append(loop.create_task(get_guids(guids,
                                                    responses,
                                                    len(replay_ids))))

            await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main([], asyncio.Queue()))
```
