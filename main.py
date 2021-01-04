from flask import Flask
import requests as r, re
from flask import request
import json, base64
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
def home():
	return "ONLINE"


@app.route('/api/add', methods=['GET'])
def fb():
	url = request.args.get('url')
	req = r.get(url)
	sd = re.search('sd_src:"(.+?)"', req.text).group(1)
	hd = re.search('hd_src:"(.+?)"', req.text).group(1)
	js = {"results-hd": hd, "results-sd": sd}
	return js


@app.route('/lirik', methods=['GET'])
def lirik():
	artis = request.args.get('artis')
	judul = request.args.get('judul')
	print('https://lirik.id/lyric/' + artis + '-' + judul)
	req = r.get('https://lirik.id/lyric/' + judul + '-' + artis)
	soup = BeautifulSoup(req.text, 'html.parser')
	car = soup.find('div', class_='entry-content')
	js = {"Hasil": car.text}
	return js


@app.route('/nulis', methods=['GET'])
def tulis():
	from nulis import tulis
	text = request.args.get('text')
	tulis = tulis(text)
	for i in tulis.tulis():
		i.save('gambar.jpg')
		image = open('gambar.jpg', 'rb')
		image_read = image.read()
		image_64_encode = base64.encodebytes(image_read)
		url = 'https://api.imgbb.com/1/upload'
		par = {
		    'key': 'b76b9a5f05dafad41987044532b9e400',
		    'image': image_64_encode,
		    'name': 'nulis',
		    'expiration': 60
		}
		headers = {'Accept': 'application/json'}
		req = r.post(url, data=par, headers=headers)
		p = req.json()['data']['display_url']
		js = {"results": p}
		return js


@app.route('/ig', methods=['GET'])
def ig():
	url = request.args.get('video_id')
	req = r.get('https://instagram.com/p/' + url + '?__a=1')
	jss = req.json()['graphql']['shortcode_media']['video_url']
	js = {"results": jss}
	return js


if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0")
