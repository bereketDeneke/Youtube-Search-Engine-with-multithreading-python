'''
Author: Bereket Siraw
Date: 03/25/2021 GC.
Updated: 8/6/2021 
newFeature: adding mulit-threading concept to reduce time complexity
Purpose: It's aim is to serve mimic and fetch data from youtube without the use of api
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
        self.limit = 10 #no limit
        self.timeout = 10 # 10sec

    def encode(self, val):
        return str(val).replace(" ", "+")

    def filter(self, val):
        return val[0:str(val).find('''"''')]

    def request_hundler(self,key):
        req = requests.get("https://www.youtube.com/results?search_query="+key)
        return req.content.decode()


    def leak_yt_url(self, video_id, caption="notSet"):
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
            # except Exception as e:
            #     print("Error:) on line 47 "+str(e))
        return [download_url, video_id]

    def searchin(self):
        obj = {}
        his = []
        
        encode_keyword = self.encode(self.keyword)
        html = self.request_hundler(encode_keyword)
        video = re.findall(r"videoId\":\"(\S{11})", html)
        video = list(set(video))  # dublicate removed
        # txt = re.findall(r"\"ownerText\":{\"runs\":\[{\"text\":\"(\S{20})", html) 
        # txt = list(set(txt))
        video = video[:self.limit]
        # txt = txt[:self.limit]

        with ThreadPoolExecutor(max_workers=100) as excutor: 
            his = excutor.map(self.leak_yt_url, video)
            obj = {"inf":[{"txt":ret} for ret in his]}

            if hasattr(obj, 'inf'):
                if len(obj.inf) == 0 and "Result is not found" not in html:
                    print("Ohoo testy ha:) ")
                    return searchin(keyword)
            return obj


# MSSQLSERVER
# typewriter
#port number to communicate with master node 8391
#master nodee https://bereket-siraw:8391
# controller name: bereket

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
