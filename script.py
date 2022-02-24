import math
import urllib
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import re
from urllib.parse import quote


metaData = ["geonameid", "name", "asciiname", "alternatenames", "latitude", "longitude", "feature class",
                    "feature code", "country code", "cc2", "admin1 code", "admin2 code", "admin3 code", "admin4 code", "population", "elevation", "dem", "timezone", "modification date"]


class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if None != re.search('/geonameid/*', self.path):
            geonameid = self.path.split('/')[-1]
            cityData = get_city_data(str(geonameid))
            self.wfile.write('<html><head><meta charset="utf-8"><body style="white-space: pre-line">'.encode())

            if cityData == -1:
                self.wfile.write("Error: invalid geonameid</body></html>".encode())
                return

            for i in range(len(metaData)):
                if cityData[i] != "":
                    self.wfile.write((str(metaData[i]) + ": " + str(cityData[i]) + "\n").encode())
            self.wfile.write("</body></html>".encode())
            return

        if None != re.search('/page/*', self.path):
            pnANDcn = self.path.split('/')[-1].split('+')
            citiesData = get_page_cites_data(int(pnANDcn[0]), int(pnANDcn[-1]))
            self.wfile.write('<html><head><meta charset="utf-8"><body style="white-space: pre-line">'.encode())

            if citiesData == -1:
                self.wfile.write("Error: invalid page number or number of cities</body></html>".encode())
                return

            for countCity in range(len(citiesData)):
                for countData in range(len(citiesData[countCity])):
                    if citiesData[countCity][countData] != "":
                        self.wfile.write((str(metaData[countData]) + ": " + str(citiesData[countCity][countData]) + "\n").encode())
            self.wfile.write("</body></html>".encode())
            return

        if None != re.search('/ru/*', self.path):
            cities = self.path.split('/')[-1].split('+')
            comparison, citiesData = get_data_ru(str(urllib.parse.unquote(cities[0])), str(urllib.parse.unquote(cities[1])))
            self.wfile.write('<html><head><meta charset="utf-8"><body style="white-space: pre-line">'.encode())

            if citiesData == -1:
                self.wfile.write("Error: invalid names of cities</body></html>".encode())
                return

            self.wfile.write((str(comparison) + "\n\n").encode())

            for countCity in range(len(citiesData)):
                for countData in range(len(citiesData[countCity])):
                    if citiesData[countCity][countData] != "":
                        self.wfile.write((str(metaData[countData]) + ": " + str(citiesData[countCity][countData]) + "\n").encode())
            self.wfile.write("</body></html>".encode())
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write('<html><head><meta charset="utf-8">'.encode())
        self.wfile.write('<title>HTTP-сервер.</title></head>'.encode())
        self.wfile.write('<body>GET-запрос</body></html>'.encode())
        return


def get_city_data(geonameid):
    with open("RU.txt", "r", encoding='utf-8') as file:
        for line in file:
            if geonameid in line.split("\t"):
                return line.split("\t")
        return -1


def get_page_cites_data(pageNum, citiesNum):
    linesNum = sum(1 for line in open("RU.txt", "r", encoding='utf-8'))
    lineNum = pageNum * citiesNum - citiesNum - 1

    if lineNum > linesNum or pageNum < 1 or citiesNum < 1:
        return -1

    result = []

    with open("RU.txt", "r", encoding='utf-8') as fp:
        for countLine, line in enumerate(fp):
            if countLine > lineNum:
                result.append(line.split("\t"))
            if countLine > lineNum + citiesNum - 1:
                return result
    return -1


def get_data_ru(city1, city2):
    resCity1 = []
    resCity2 = []

    with open("RU.txt", "r", encoding='utf-8') as file:
        for line in file:
            if city1 in line.split("\t")[3].split(","):
                resCity1.append(line.split("\t"))

            if city2 in line.split("\t")[3].split(","):
                resCity2.append(line.split("\t"))

    if not resCity1 or not resCity2:
        return -1

    latitude1, timezone1, longitude1 = search_max_pop(resCity1)
    latitude2, timezone2, longitude2 = search_max_pop(resCity2)

    if latitude1 - latitude2 > 0:
        comparison = city1 + " north of " + city2
    else:
        comparison = city2 + " north of " + city1

    comparison += ","

    if timezone1 == timezone2:
        comparison += " same time zone"
    else:

        comparison += " time zones differ by " + str(abs(math.floor((longitude1 - longitude2) / 15))) + " hours"

    return comparison, resCity1 + resCity2


def search_max_pop(cities):
    maxPop = -1
    latitude = 0
    longitude = 0
    timezone = ""
    q = 0
    for city in cities:
        if maxPop < int(city[-5]):
            maxPop = int(city[-5])
            latitude = float(city[4])
            longitude = float(city[5])
            timezone = str(city[-2])
    return latitude, timezone, longitude


def run(server_class=HTTPServer, handler_class=HttpGetHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


run()
