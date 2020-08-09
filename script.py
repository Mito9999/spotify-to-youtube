from requests import get
from bs4 import BeautifulSoup
from json import loads
from youtubesearchpython import SearchVideos



# gets the spotify links from songs file
with open('songs.txt', 'r') as songs_file:
    spotify_links = songs_file.readlines()

# the instrumentals.txt file is where all of the instrumental song links will be stored
instrumentals_file = open('instrumentals.txt', 'w')

for i in range(len(spotify_links)):
    # this is a bit unnecesary, will make this better in the next version
    song_id = ''.join(spotify_links[i]).split('https://open.spotify.com/track/')[1].split('\n')[0]
    lnk = f'https://open.spotify.com/track/{song_id}'

    # scrapes the HTML of the spotify track, and gets the title
    source = get(lnk).text
    soup = BeautifulSoup(source, 'lxml')
    spotify_song_title = soup.find("title").text
    title = spotify_song_title.split(', a song')
    youtube_search_title = f"{title[0]}{title[1].split(' on Spotify')[0]} instrumental"
    print(f"Searching for: {youtube_search_title}")


    search = loads(SearchVideos(youtube_search_title, offset = 1, mode = "json", max_results = 1).result())
    ytLink = search['search_result'][0]['link']
    print(ytLink)
    instrumentals_file.write(f"{ytLink}\n")

    print(f"FOUND: {search['search_result'][0]['title']}")

instrumentals_file.close()