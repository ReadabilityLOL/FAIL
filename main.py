import feedparser
from flask import Flask, render_template, request
import textwrap
import ast

style = """
*{font-family: "Handlee", serif; font-weight: 400; font-style: normal;}
.title{margin:2%; padding-left:8%; font-size:2.5ch; line-height:3.6ch%;}
img{/*margin-right:15px !important;*/ width: 0px; height: 0; object-fit: contain; float: left;}
.description{text-align:justify; margin-left:10%}
.entry{border: solid black; border-radius: 2px; padding-bottom: 1%; padding-left: 2%; padding-right: 5%; width: 50%; margin:auto; margin-bottom:1%; 
  border-radius: 255px 15px 225px 15px/15px 225px 15px 255px;
  line-height:1.5em;
  border:solid;
}
.header{style: bold; font-size:10ch; text-align: center; margin-bottom:0px;}
.otherpage{text-decoration: none; margin-bottom:1.5%; text-align:center;}
"""

class siteFeed:
  def __init__(self,url,numEntries=5):
    self.url = url
    self.feed = feedparser.parse(url)
    self.numEntries = numEntries
  
  def getEntries(self):
      return self.feed.entries[:self.numEntries]
  
  def formatEntry(self,entry):
    return textwrap.dedent(
    f"""
    <div class="entries">
      <div class="entry">
        <div class="title">
          <a class="link" href={entry["link"]}> {entry["title"]}</a> - <a class="website" href={self.feed.channel["link"]}>{self.feed.channel["title"]}</a>
        </div>
        <div class="description">
          {entry["description"]}
        </div>
      </div>
    </div>
    """
    )

app = Flask(__name__)

def getEntries():
  entries = ""
  entry_list = []
  with open("links.txt","r") as file:
    for x in file.readlines():
      r = siteFeed(x)
      for y in r.getEntries():
        entry_list.append([y.published_parsed,r.formatEntry(y)]) 
    for x in sorted(entry_list,key=lambda y:y[0],reverse=True):
      entries += x[1]
    return entries

#html = f"""
#<!DOCTYPE html>
#<html>
#  <head lang="en">
#    <meta charset="utf-8">
#    <title>Ze grand rss feed</title>
#    <link rel="icon" href="/static/favicon.ico">
#    <link rel="preconnect" href="https://fonts.googleapis.com">
#    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
#    <link href="https://fonts.googleapis.com/css2?family=Handlee&display=swap" rel="stylesheet">
#    <style>
#    {style}
#    </style>
#  </head>
#  <body>
#    <h1 class="header">
#      F.A.I.L
#    </h1>
#    {getEntries()}
#  </body>
#</html>
#"""

def getHtml():
  html = f"""
  <!DOCTYPE html>
  <html>
    <head lang="en">
      <meta charset="utf-8">
      <title>Ze grand rss feed</title>
      <link rel="icon" href="/static/favicon.ico">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Handlee&display=swap" rel="stylesheet">
      <style>
      {style}
      </style>
    </head>
    <body>
      <h1 class="header">
        F.A.I.L
      </h1>
      <div class="otherpage"><a class="otherpage" href="/edit_feed">(press me to edit the feed)</a></div>
      <p></p>
      {getEntries()}
    </body>
  </html>
  """
  return html

@app.route("/")
def homepage(): 
  return getHtml()

@app.route("/edit_feed", methods=["POST","HEAD","OPTIONS","GET"])
def edit_feed():
  if request.method == 'POST':
    theList = ast.literal_eval(request.data.decode())
    with open("links.txt","w") as file:
      file.write("\n".join(theList)+"\n")
  lines2 = []
  with open("links.txt","r") as file:
    lines = file.readlines()
    for x in lines:
      lines2.append(f"""{x.replace("\n","")}""")

  return render_template("edit.html", feedList=lines2)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8002, debug=True)
