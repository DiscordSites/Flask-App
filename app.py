from pymongo import MongoClient
import json

with open("config.json") as conf:
    config = json.load(conf)
    database = config["database"]

client = MongoClient()
db = client["discordsites"]
doc = db["guilds"]

from flask import Flask, render_template, redirect
application = Flask(__name__, static_url_path="/static")
application.config["PROPAGATE_EXCEPTIONS"] = True

@application.route("/")
def index():
    return render_template("index.html")

@application.route("/guild/<int:guild_id>/")
def guild(guild_id):
    if doc.find_one({"guild_id": guild_id}) is None:
        return redirect("https://discordsites.me/", code=302)
    info = doc.find_one({"guild_id": guild_id})
    if info["toggle"] == 0:
        return redirect("https://discordsites.me/", code=302)
    guild_name = info["guild_name"]
    guild_icon = info["guild_icon"]
    guild_invite = info["guild_invite"]
    guild_description = info["guild_description"]
    guild_background = info["guild_background"]
    guild_membercount = info["guild_membercount"]
    return render_template("guild.html", guild_name=guild_name, guild_icon=guild_icon, guild_invite=guild_invite, guild_description=guild_description, guild_background=guild_background, guild_membercount=guild_membercount)

if __name__ == "__main__":
    application.run(host="0.0.0.0")
