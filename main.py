import pychromecast
from pychromecast import quick_play
import time

chromecasts, browser = pychromecast.get_listed_chromecasts(
    friendly_names=["Chromecast HD"]
)


cast = chromecasts[0]
print(cast.status)

cast.wait()
print(cast.status)

mc = cast.media_controller
mc.play_media('http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', 'video/mp4')
mc.block_until_active()

time.sleep(10)

browser.stop_discovery()