from getpass import getpass
# Not tried yet:
# - pip install IpCamPy
# - https://stackoverflow.com/questions/49978705/access-ip-camera-in-python-opencv

# for other "magic url formats, see
qualities = ["Motion", "Standard"]
resolutions = ["640x480", "320x240"]
quality = qualities[0]
resolution = resolutions[0]
ip = input("IP: ")
username = input("Username: ")
password = getpass()
# NOTE: http://{u}:{p}@ format will not work with urlopen.
# See HTTPBasicAuth further down instead.
url = "http://{ip}/SnapShotJPEG?Resolution={r}&Quality={q}".format(
    ip = ip,
    r = resolution,
    q = quality
)
# See
# <https://www.daniweb.com/programming/software-development/code/493004/display-an-image-from-the-web-pygame>

import io
import pygame as pg


try:
    # Python2
    from urllib2 import urlopen
except ImportError:
    # Python3
    from urllib.request import urlopen
# initialize pygame
pg.init()
pg.display.set_caption("PySecurityCam by Poikilos")

image_url = url

# import http
# try:
    # image_str = urlopen(image_url).read()
# except http.client.InvalidURL:
    # # Hide the exception, since invalid URL may contain password after
    # # colon instead of port.
    # print("The URL is incorrect (colon must be followed by port#)")
    # exit(1)
# - urlopen is only possible if no authentication (the url must have a
#   port not a password after ":" if any ":")

import requests
from requests.auth import HTTPBasicAuth

resolution_pair = resolution.split("x")
resolution_pair = int(resolution_pair[0]), int(resolution_pair[1])

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
screen = pg.display.set_mode(resolution_pair,  pg.RESIZABLE )

def show_error(msg, color=red):
    # print(msg)
    font = pg.font.Font('freesansbold.ttf', 16)
    # render(text, antialias, color, background=None) -> Surface
    lines = msg.split("\n")
    textRect = None
    for line in lines:
        text = font.render(line, True, color, black)
        if textRect is None:
            textRect = text.get_rect()
            textRect.center = (resolution_pair[0] // 2, resolution_pair[1] // 2)
        else:
            textRect = textRect.move((0, text.get_rect().height))
        screen.blit(text, textRect)

image = None
ok = None
def show_next():
    global image
    # urlopen doesn't work since security cameras require http authentication.
    # See https://stackoverflow.com/questions/24835100/getting-a-file-from-an-authenticated-site-with-python-urllib-urllib2
    r = None
    if image is None:
        if ok is None:
            show_error("Loading {}...".format(ip), color=(255,255,255))
            pg.display.flip()
    try:
        r = requests.get(url, auth=HTTPBasicAuth(username, password))
    except requests.exceptions.ConnectionError:
        screen.fill(black)
        show_error("The URL is unreachable.")
        return False
    # See https://stackoverflow.com/questions/31708519/request-returns-bytes-and-im-failing-to-decode-them
    if r.status_code == 200:
        image_str = r.content

        image_file = io.BytesIO(image_str)
        # (r, g, b) color tuple, values 0 to 255
        # create a 600x400 white screen
        screen.fill(black)

        # load the image from a file or stream
        try:
            image = pg.image.load(image_file)
        except:
            msg = "Invalid URL or login"
            screen.fill(black)
            show_error(msg)
            return False
        # image, position
        screen.blit(image, (0, 0))
        # nothing gets displayed until one updates the screen
        # start event loop and wait until
        # the user clicks on the window corner x to exit
    else:
        screen.fill(black)
        show_error("{}: Login is bad apparently otherwise get correct url from\nhttp://www.ispyconnect.com/man.aspx?n=panasonic&page=5#".format(r.status_code))
        # bad login, otherwise an error would have occured earlier
        return False
    return True

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    ok = show_next()
    pg.display.flip()
