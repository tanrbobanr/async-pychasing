import sys
sys.path.append(".")
from src import async_pychasing
import aiohttp
import pychasing
import asyncio


TOKEN              = ""
STEAM_ID           = ""
REPLAY_PATH        = "tests/test_replay.replay"
GROUP_NAME         = "__pychasing_test_group__"
REPLAY_NAME        = "__pychasing_test_replay__"
UPLOADED_REPLAY_ID = ""


pychasing_client = async_pychasing.Client(
    TOKEN,
    True,
    pychasing.PatreonTier.none
)


async def test_ping(session: async_pychasing.Session) -> None:
    """Test the `async_pychasing.client.Session.ping` method."""
    res0 = await session.ping()
    json0 = await res0.json()
    print(json0)
    assert json0["chaser"] is True
    print("\033[96masync_pychasing.client.Session.ping \033[90m: \033[92mGOOD\033[0m")


async def test_list_replays(session: async_pychasing.Session) -> None:
    res0 = await session.list_replays(count=5, pro=True, playlists=[pychasing.Playlist.ranked_doubles])
    json0 = await res0.json()
    assert len(json0["list"]) == 5
    res1 = await session.list_replays(next = json0["next"])
    json1 = await res1.json()
    print(json1)
    assert len(json1["list"]) == 5
    assert json0["list"][0]["id"] != json1["list"][0]["id"]
    print("\033[96masync_pychasing.client.Session.list_replays \033[90m: \033[92mGOOD\033[0m")


async def test_list_groups(session: async_pychasing.Session) -> None:
    res0 = await session.list_groups(count=5)
    json0 = await res0.json()
    print(json0)
    assert len(json0["list"]) == 5
    res1 = await session.list_groups(next=json0["next"])
    json1 = await res1.json()
    print(json1)
    assert len(json1["list"]) == 5
    assert json0["list"][0]["id"] != json1["list"][0]["id"]
    print("\033[96masync_pychasing.client.Session.list_groups \033[90m: \033[92mGOOD\033[0m")


async def test_maps(session: async_pychasing.Session) -> None:
    res0 = await session.maps()
    json0 = await res0.json()
    print(json0)
    assert json0["arc_standard_p"] == "Starbase ARC (Standard)"
    print("\033[96masync_pychasing.client.Session.maps \033[90m: \033[92mGOOD\033[0m")


async def test_create_group(session: async_pychasing.Session) -> None:
    res0 = await session.create_group(GROUP_NAME, pychasing.PlayerIdentification.by_id, pychasing.TeamIdentification.by_player_clusters)
    json0 = await res0.json()
    print(json0)
    assert "https://ballchasing.com/api/groups/" in json0["link"]
    print("\033[96masync_pychasing.client.Session.create_group \033[90m: \033[92mGOOD\033[0m")


async def test_upload_replay(session: async_pychasing.Session) -> None:
    groups = await session.list_groups(name=GROUP_NAME, creator=STEAM_ID)
    groups_json = await groups.json()
    with open(REPLAY_PATH, "rb") as replay_file:
        res0 = await session.upload_replay(replay_file, pychasing.Visibility.private, group = groups_json["list"][0]["id"])
        json0 = await res0.json()
    print(json0)
    print(f"\033[96masync_pychasing.client.Session.upload_replay \033[90m: \033[92mGOOD\033[0m\n\nNEW REPLAY ID: {json0['id']}")


async def test_get_replay(session: async_pychasing.Session) -> None:
    res0 = await session.get_replay(UPLOADED_REPLAY_ID)
    json0 = await res0.json()
    print(json0)
    assert json0["id"] == UPLOADED_REPLAY_ID
    print("\033[96masync_pychasing.client.Session.get_replay \033[90m: \033[92mGOOD\033[0m")


async def test_get_group(session: async_pychasing.Session) -> None:
    groups = await session.list_groups(name=GROUP_NAME, creator=STEAM_ID)
    groups_json = await groups.json()
    res0 = await session.get_group(groups_json["list"][0]["id"])
    json0 = await res0.json()
    print(json0)
    assert json0["name"] == GROUP_NAME
    print("\033[96masync_pychasing.client.Session.get_group \033[90m: \033[92mGOOD\033[0m")


async def test_patch_group(session: async_pychasing.Session) -> None:
    groups = await session.list_groups(name=GROUP_NAME, creator=STEAM_ID)
    groups_json = await groups.json()
    res0 = await session.patch_group(groups_json["list"][0]["id"], team_identification=pychasing.TeamIdentification.by_distinct_players)
    text0 = await res0.text()
    print(text0)
    assert text0 == ""
    res1 = await session.get_group(groups_json["list"][0]["id"])
    json1 = await res1.json()
    print(json1)
    assert json1["team_identification"] == pychasing.TeamIdentification.by_distinct_players.value
    print("\033[96masync_pychasing.client.Session.patch_group \033[90m: \033[92mGOOD\033[0m")


async def test_patch_replay(session: async_pychasing.Session) -> None:
    res0 = await session.patch_replay(UPLOADED_REPLAY_ID, title=REPLAY_NAME, visibility=pychasing.Visibility.public)
    text0 = await res0.text()
    print(text0)
    assert text0 == ""
    res1 = await session.get_replay(UPLOADED_REPLAY_ID)
    json1 = await res1.json()
    print(json1)
    assert json1["title"] == REPLAY_NAME
    print("\033[96masync_pychasing.client.Session.patch_replay \033[90m: \033[92mGOOD\033[0m")


async def test_download_replay(session: async_pychasing.Session) -> None:
    with open(REPLAY_PATH, "rb") as replay_file:
        res0 = await session.download_replay(UPLOADED_REPLAY_ID)
        async for c in res0.content.iter_chunked(100):
            chunk = c
            print(chunk)
            break
        print(replay_file.read(100))
        replay_file.seek(0)
        assert chunk == replay_file.read(100)
    print("\033[96masync_pychasing.client.Session.download_replay \033[90m: \033[92mGOOD\033[0m")


async def test_experimentals(session: async_pychasing.Session) -> None:
    res0 = await session.get_threejs(UPLOADED_REPLAY_ID)
    print(await res0.content.read(100))
    input("\033[92mPress any key to continue...\033[0m")
    res1 = await session.get_timeline(UPLOADED_REPLAY_ID)
    print(await res1.content.read(100))
    input("\033[92mPress any key to continue...\033[0m")
    groups = await session.list_groups(name=GROUP_NAME, creator=STEAM_ID)
    groups_json = await groups.json()
    res2 = await session.export_csv(groups_json["list"][0]["id"], pychasing.GroupStats.players)
    print(await res2.content.read(100))


async def test_delete_replay(session: async_pychasing.Session) -> None:
    res0 = await session.delete_replay(UPLOADED_REPLAY_ID)
    text0 = await res0.text()
    print(text0)
    assert text0 == ""
    print("\033[96masync_pychasing.client.Session.delete_replay \033[90m: \033[92mGOOD\033[0m")


async def test_delete_group(session: async_pychasing.Session) -> None:
    groups = await session.list_groups(name=GROUP_NAME, creator=STEAM_ID)
    groups_json = await groups.json()
    res0 = await session.delete_group(groups_json["list"][0]["id"])
    text0 = await res0.text()
    print(text0)
    assert text0 == ""
    print("\033[96masync_pychasing.client.Session.delete_group \033[90m: \033[92mGOOD\033[0m")


async def main(step: int) -> None:
    async with aiohttp.ClientSession() as cs:
        async with pychasing_client(cs) as ps:
            if step == 0: await test_ping(ps)
            if step == 1: await test_list_replays(ps)
            if step == 2: await test_list_groups(ps)
            if step == 3: await test_maps(ps)
            if step == 4: await test_create_group(ps)
            if step == 5: await test_upload_replay(ps)
            if step == 6: await test_get_replay(ps)
            if step == 7: await test_get_group(ps)
            if step == 8: await test_patch_group(ps)
            if step == 9: await test_patch_replay(ps)
            if step == 10: await test_download_replay(ps)
            if step == 11: await test_experimentals(ps)
            if step == 12: await test_delete_replay(ps)
            if step == 13: await test_delete_group(ps)
            if step == 14: print("DONE!")


if __name__ == "__main__":
    step = 0
    asyncio.run(main(step))
