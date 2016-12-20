# Twitch.tv Plugin
# v0.1 by Marshall Thornton <marshallthornton@gmail.com>
# Code inspired by Justin.tv plugin by Trevor Cortez and John Roberts
# v0.2 by Nicolas Aravena <mhobbit@gmail.com>
# Adaptation of v0.1 for new Plex Media Server.

####################################################################################################

REST_API_FILMS = 'http://localhost:8087/films';
REST_API_THUMBNAIL = 'http://localhost:8087/thumbnail?link=%s';
TWITCH_FEATURED_STREAMS = 'https://api.twitch.tv/kraken/streams/featured'
TWITCH_TOP_GAMES = 'https://api.twitch.tv/kraken/games/top'
TWITCH_LIST_STREAMS = 'https://api.twitch.tv/kraken/streams'
TWITCH_SEARCH_STREAMS = 'https://api.twitch.tv/kraken/search/streams'
CLIENT_ID = 'gzux2tt85x9ppnnxyh7czkfiovtxtd7'
PAGE_LIMIT = 50
NAME = 'HDFilme'

####################################################################################################
def Start():

	ObjectContainer.title1 = NAME
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'
	HTTP.Headers['Client-ID'] = CLIENT_ID
	HTTP.CacheTime = 300

####################################################################################################
@handler('/video/hdfilme', NAME)
def MainMenu(**kwargs):

	oc = ObjectContainer()
	oc.add(DirectoryObject(key=Callback(Filme), title="Filme"))
	Log("b")

	return oc

####################################################################################################
@route('/video/hdfilme/featured')
def Filme():
	Log("a")

	oc = ObjectContainer(title2="Featured Streams", no_cache=True)
	url = REST_API_FILMS
	filmData = JSON.ObjectFromURL(REST_API_FILMS)
	
	currentPage = filmData['currentSite']
	maxPages = filmData['maxSite']
	
	for film in filmData['filmInfo']:
		Log(film['url'])
		oc.add(VideoClipObject(
			title = film['title'],
			summary = film['description'],
			#thumb = Resource.ContentsOfURLWithFallback(film['imageUrl']),
			url = film['url'],
			thumb = Resource.ContentsOfURLWithFallback(REST_API_THUMBNAIL % (film['url']))
		))

	'''for stream in featured['featured']:
		summary = String.StripTags(stream['text'])

		if stream['stream']['game']:
			subtitle = "%s\n%s Viewers" % (stream['stream']['game'], stream['stream']['viewers'])
		else:
			subtitle = "%s Viewers" % (stream['stream']['viewers'])
		Log(stream)
		Log(stream['stream']['channel']['url'])
		oc.add(VideoClipObject(
			url = stream['stream']['channel']['url'],
			title = stream['stream']['channel']['display_name'],
			summary = '%s\n\n%s' % (subtitle, summary),
			thumb = Resource.ContentsOfURLWithFallback(stream['stream']['preview']['large'])
		))'''

	return oc
