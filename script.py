from requests import get
from time import sleep
from bs4 import BeautifulSoup
from youtube_search import YoutubeSearch
from json import loads


# gets the spotify links from songs file
with open('songs.txt', 'r') as songsFile:
    spotifyLinks = songsFile.readlines()

# the instrumentals.txt file is where all of the instrumental song links will be stored
instrumentalsFile = open('instrumentals.txt', 'w')

for i in range(len(spotifyLinks)):
    # this is a bit unnecesary, will make this better in the next version
    song_id = ''.join(spotifyLinks[i]).split('https://open.spotify.com/track/')[1].split('\n')[0]
    lnk = f'https://open.spotify.com/track/{song_id}'

    # scrapes the HTML of the spotify track, and gets the title
    source = get(lnk).text
    soup = BeautifulSoup(source, 'lxml')
    spotifySongTitle = soup.find("title").text
    title = spotifySongTitle.split(', a song')
    youtubeSearchTitle = f"{title[0]}{title[1].split(' on Spotify')[0]} instrumental"
    print(f"Searching for: {youtubeSearchTitle}")


    # YoutubeSearch sometimes returns an empty list, so this just makes it constantly try to find the instrumental
    while True:
        try:
            results = loads(YoutubeSearch(youtubeSearchTitle, max_results=1).to_json())
            ytLink = f"youtube.com{results['videos'][0]['link']}"
            instrumentalsFile.write(f"{ytLink}\n")
            break
        except IndexError:
            pass
    print(f"FOUND: {results['videos'][0]['title']}")

instrumentalsFile.close()