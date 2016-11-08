#This code is written in Python3.
#Importing the necessary modules.
import requests
import re
from pytube import YouTube
import sys

#Providing a path to the configuration file. This stores the path 
#to the directory where the downloads are installed.
CONFIG_FILE = 'CONFIG_FILE.txt'
path = ''
new = []

#Get the source code of the youtube playlist URL.
def get_source_html():
	page_content = requests.get(sys.argv[1])
	source_code = str(page_content.content)
	return source_code

#Find all the videos of the playlist.
def parse_source_html(source_code):
	vid_url_pat = re.compile(r'watch\?v=\S+index=\d\d?')
	vid_url_matches = list(set(re.findall(vid_url_pat,source_code)))
	return vid_url_matches

#Prefix the matches to complete the link
def add_prefixes(vid_url_matches):
	for link in (vid_url_matches):
		new.append('https://www.youtube.com/' + link)
	return new	

#Downloading the video with the help of the module PyTube
def download(new,path):
	for things in new:
		yt = YouTube(things)

		#This only tries to download a 720p version of the video
		try:
			video = yt.get('mp4', '720p')
		except:
			print("Cannot find 720p version of video")

		try:
			print("trying to download", yt.filename + " Video...")
			video.download(path)
			print("Download Successful!")
		except OSError:
			print(yt.filename, "already exists in the Directory! Skipping video...")

#This ensures that the code can be imported as a module
if __name__ == '__main__':

	#On the second run of the program, the path need not be entered as the path of the
	#previous run is stored in the CONFIG_FILE file.
	try:
		with open(CONFIG_FILE, 'r') as f:
			path = f.read()
	except IOError as e:
		print ("I/O error({0}): {1}".format(e.errno, e.strerror))
		exit(1)

	#Writes the specified path to the CONFIG_FILE file.
	if len(sys.argv) == 3:
		path = sys.argv[2]
		with open(CONFIG_FILE, 'w') as f:
			f.write(path)
			f.close()
	
	#Ensures that the correct number of arguments are passed in.
	if len(sys.argv) < 2 or len(sys.argv) > 3:
		print("Usage: python3 Downloader.py playlistURL OR python3 Downloader.py playlistURL destPath")
		exit(1)

	#Checks whether path has been entered and if not tells the user to enter the path.
	if not path:
		print("Please specify the path")
		exit(1)
	
	
	whole = get_source_html()
	youtube_videos = parse_source_html(whole)
	final = add_prefixes(youtube_videos)
	download(final,path)
	
	







	
