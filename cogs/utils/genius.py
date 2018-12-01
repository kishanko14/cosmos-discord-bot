import lyricsgenius as genius
from cogs.utils import util
from cogs.utils.paginator import Pages


_CAT = util.get_config()["GENIUS_CLIENT_ACCESS_TOKEN"]

class Genius(object):
    """Fetch lyrics, artists and song info from Genius."""

    def __init__(self, ctx, query):
        self.client = genius.Genius(_CAT)
        self.ctx = ctx
        self.query = query
        self.song = self.client.search_song(self.query)
        self.page = None

    async def show_song_lyrics(self):
        try:
            self.page = Pages(self.ctx, entries=self.song.lyrics.split("\n"), show_entry_count=False, timeout=300, show_author=False, per_page=27)
        except:
            await self.ctx.send("Lyrics not found ;-;")
            return
        self.page.embed.title = f"{self.song.title} - Lyrics"
        self.page.embed.set_author(name=self.song.artist, icon_url=self.song.song_art_image_url)
        await self.page.paginate()