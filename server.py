'''
Author: Bereket Siraw
Date: 03/25/2021 GC
Updated: 8/6/2021 GC
Purpose: It aims to fetch data from youtube without the use of api and remove unwanted ads.
'''
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from waitress import serve
from flask import Flask
from flask import render_template, request, redirect, make_response
from flask_cors import CORS
import requests
import re
import pafy
from time import sleep, perf_counter

app = Flask(__name__)
CORS(app)

class youtubeHundler:
    def __init__(self, keyword):
        self.keyword = keyword
        self.limit = 10 
        self.timeout = 10 

    def encode(self, val):
        return str(val).replace(" ", "+")

    def filter(self, val):
        return val[0:str(val).find('''"''')]

    def request_hundler(self,key):
        req = requests.get("https://www.youtube.com/results?search_query="+key)
        return req.content.decode()


    def get_url(self, video_id, caption="notSet"):
        download_url = None
        if len(video_id)==0:
            return [download_url, video_id, caption]
        try: 
            req = requests.get("https://www.youtube.com/watch?v="+video_id)
            content = req.content.decode()
            url = re.findall(r"itag\":18\,\"url\":\"(.*?)\"", content)
            if len(url)!=0:
                download_url =  str(url[0]).replace("\\u0026", "&")
        except:
            video = pafy.new("https://youtu.be/{}".format(video_id))
            best = video.getbest()
            download_url = best.url
        return [download_url, video_id]

    def searchin(self):
        obj = {}
        his = []
        
        encode_keyword = self.encode(self.keyword)
        html = self.request_hundler(encode_keyword)
        video = re.findall(r"videoId\":\"(\S{11})", html)
        video = list(set(video)) 
        video = video[:self.limit]

        with ThreadPoolExecutor(max_workers=100) as excutor: 
            his = excutor.map(self.get_url, video)
            obj = {"inf":[{"txt":ret} for ret in his]}

            if hasattr(obj, 'inf'):
                if len(obj.inf) == 0 and "Result is not found" not in html:
                    print("Result is found!")
                    return searchin(keyword)
            return obj

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/api/search=<keyword>')
def search(keyword):
    youtube = youtubeHundler(keyword)
    if len(keyword.strip()) > 0:
        url = youtube.searchin()
        return make_response(url, 200)
    return {"info": "bad request"}

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", message=e)

if __name__ == '__main__':
    app.run(debug=False, threaded=True)
    serve(app, host='0.0.0.0', port=80)
