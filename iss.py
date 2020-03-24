#!/usr/bin/env python

__author__ = 'Sean Bailey, Koren, Chris Wilson, Arnold Schwarzenegger, Kano'


import requests
import turtle
import time


def get_astro():
    astro = requests.get("http://api.open-notify.org/astros.json")
    astro = astro.json()
    print("Astronauts: ")
    for person in astro["people"]:
        print("  {} is currently on the {}.".format(
            person["name"], person["craft"]))
    print("There are {} people on the ISS right now.".format(
        len(astro["people"])))


def get_iss_coordinates():
    coords = requests.get("http://api.open-notify.org/iss-now.json")
    coords = coords.json()
    longi = coords[u"iss_position"][u"longitude"]
    lat = coords[u"iss_position"][u"latitude"]
    print(" ")
    print("The ISS is at longitude {} and latitude {} as of {}.".format(
        longi, lat, time.ctime(coords[u"timestamp"])))
    return [float(longi), float(lat)]


def draw_iss(coords):
    """Draws the ISS on the map where it is on program run
    and also the dot over Indy with the next time the ISS will
    be over Indy."""
    screen = turtle.Screen()
    screen.register_shape("iss.gif")
    screen.setup(width=720, height=360)
    screen.setworldcoordinates(-180, -90, 180, 90)
    iss_turtle = turtle.Turtle()
    iss_turtle.shape("iss.gif")
    iss_turtle.screen.bgpic("map.gif")
    iss_turtle.screen.title("ISS locator")
    iss_turtle.penup()
    iss_turtle.goto(coords[0], coords[1])
    iss_turtle.pendown()
    iss_over_indy(screen)
    if screen is not None:
        print('Click on screen to exit ...')
        screen.exitonclick()


def iss_over_indy(screen):
    """DOT over Indy with the date and time the ISS will
    pass over Indy"""
    pass_api = "http://api.open-notify.org/iss-pass.json?"
    indy_lat = 39.8028
    indy_longi = -86.1210
    coords = requests.get("{}lat={}&lon={}".format(
        pass_api, indy_lat, indy_longi))
    coords = coords.json()
    pass_time = time.ctime(coords[u'response'][0]["risetime"])
    indy_turtle = turtle.Turtle()
    indy_turtle.shape("circle")
    indy_turtle.color("yellow", "yellow")
    indy_turtle.penup()
    indy_turtle.goto(indy_longi, indy_lat)
    indy_turtle.pendown()
    indy_turtle.write(pass_time, align=("left"), font=(30))
    indy_turtle.penup()


def main():
    get_astro()
    coords = get_iss_coordinates()
    draw_iss(coords)


if __name__ == '__main__':
    main()
