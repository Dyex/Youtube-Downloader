import requests
import re
from pytube import YouTube
import sys

CONFIG_FILE = 'CONFIG_FILE.txt'
path = ''
new = []


def get_source_html():
	page_content = requests.get(sys.argv[1])
	compl = str(page_content.content)
	return compl

def parse_source_html(compl):
	vid_url_pat = re.compile(r'watch\?v=\S+index=\d\d?')
	vid_url_matches = list(set(re.findall(vid_url_pat,compl)))
	return vid_url_matches

def add_prefixes(vid_url_matches):
	for link in (vid_url_matches):
		new.append('https://www.youtube.com/' + link)
	return new	

def download(new,path):
	for things in new:
		yt = YouTube(things)
		try:
			video = yt.get('mp4', '360p')
		except:
			print("Cannot find 360p version of video")
		try:
			print("trying to download", yt.filename + " Video...")
			video.download(path)
			print("Download Successful!")

			
		except OSError:
			print(yt.filename, "already exists in this directory! Skipping video...")

if __name__ == '__main__':
	try:
		with open(CONFIG_FILE, 'r') as f:
			path = f.read()
	except IOError as e:
		print ("I/O error({0}): {1}".format(e.errno, e.strerror))
		exit(1)

	if len(sys.argv) == 3:
		path = sys.argv[2]
		with open(CONFIG_FILE, 'w') as f:
			f.write(path)
			f.close()
	
	if len(sys.argv) < 2 or len(sys.argv) > 3:
		print("Usage: python3 Downloader.py playlistURL OR python3 Downloader.py playlistURL destPath")
		exit(1)

	if not path:
		print("Please specify the path")
		exit(1)
	
	
	whole = get_source_html()
	youtube_videos = parse_source_html(whole)
	final = add_prefixes(youtube_videos)
	download(final,path)
	
	







	
