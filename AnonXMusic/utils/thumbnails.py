import os
import re
import textwrap

import aiofiles
import aiohttp
import numpy as np

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch

from config import YOUTUBE_IMG_URL
from AnonXMusic import app


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def clear(text):
    list = text.split(" ")
    title = ""
    for i in list:
        if len(title) + len(i) < 60:
            title += " " + i
    return title.strip()


async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(0))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(1.1)
        draw = ImageDraw.Draw(background)
        arial = ImageFont.truetype("AnonXMusic/assets/font2.ttf", 40)
        font = ImageFont.truetype("AnonXMusic/assets/font.ttf", 45)
   #     text_color = (0, 128, 0)
        draw.text((1009, 8), unidecode(app.name), fill="white", font=arial)
    #    draw.text(
    #        (55, 560),
    #        f"{channel} | {views[:23]}",
    #        (0, 128, 0), 
    #        font=arial,
          #  width=70, 
    #    )
        draw.text(
            (57, 600),
            clear(title),
            (0, 128, 0), 
            stroke_width=2,
            stroke_fill="white",
           # width=50, 
            font=font,
          #  fill="black", 
        )
        draw.line(
            [(55, 660), (1220, 660)],
            fill="Green",
            width=11,
            stroke_width=1,
            stroke_fill="white",
            joint="curve",
        )
        draw.ellipse(
            [(942, 648), (942, 672)],
            outline="black",
            fill="black", 
            width=30,
        )
        draw.text(
            (36, 670),
            "00:00",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (1185, 670),
            f"{duration[:23]}",
            (255, 255, 255),
            font=arial,
        )
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        background.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
