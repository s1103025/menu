
from flask import Flask, render_template, request, make_response, jsonify
…
@app.route("/webhook", methods=["POST"])
def webhook():
  

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


import requests
from bs4 import BeautifulSoup
url = "https://www.mos.com.tw/menu/set.aspx"
Data = requests.get(url)
Data.encoding = "utf-8"
sp = BeautifulSoup(Data.text, "html.parser")
result=sp.select(".productsList li")
info = ""
price = ""

for item in result:
  #info += item.text + "\n\n"
  title = item.find("h1")
  if title != None:
    price = item.find("span", class_="set")
    info += "\n" + "商品名稱：" + title.text + "\n\n" + "價格：" + price.text + "\n" + "商品資訊："
    titles = ""
    imgs = item.select("img")
    for img in imgs:
      if img.get("title") != None:
        titles += img.get("title")
    info += titles + "\n"
    doc = {
      "商品名稱：": title.text,
      "價格：": price.text,
      "商品資訊：": titles
    }
    collection_ref = db.collection("主餐菜單")
    collection_ref.add(doc)


  
    return make_response(jsonify({"fulfillmentText": info}))

if __name__ == "__main__":
    app.run()

#print(info)
