#! /usr/bin/python
#! -*- coding: utf-8 -*-

import webapp
import sys
import urllib


class Shortener(webapp.webApp):
    """Web application class to abbreviate urls"""
    conversions = {}
    urlList = []
    counter = 0

    def printConvertions(self):
        table = ""
        for abbr in self.conversions:
            table = table + self.conversions[abbr]
            table = table + " => "
            table = table + abbr + "<br>"

        return table

    def parse(self, request):
        """Parses the requested resource, the body
        and the verb of the HTTP request"""

        verb = request.split()[0]
        host = request.split("\n")[1].split()[1]
        resource = request.split()[1]
        body = request.split("\r\n\r\n")[1]

        return (verb, host, resource, body)

    def process(self, parsedRequest):
        """Serves a form for the '/' resource and an
        abbreviated url for any valid url given"""

        verb, host, resource, body = parsedRequest

        if verb == "GET":
            if resource == "/":
                httpCode = "200 OK"
                httpBody = ("<html><body><form action='/' method='POST'>"
                            + "Introduce your url:"
                            + "<input type='text' name='url'/></br>"
                            + "<input type='submit' value='Submit' "
                            + "/></form><br><br>"
                            + self.printConvertions()
                            + "</body></html>")
            else:
                urlsh = "http://" + host + resource
                if urlsh in self.conversions:
                    httpCode = "200 OK"
                    httpBody = ("<html><body><meta http-equiv='refresh'"
                                + "content='0;" + " url="
                                + self.conversions[urlsh]
                                + "' /></body></html>")
                else:
                    httpCode = "404 Not Found"
                    httpBody = ("<html><body><h3>"
                                + "404 Not available resource"
                                + "</h3></body></html>")

        elif verb == "POST":
            if resource == "/":
                httpCode = "200 OK"
                url = urllib.unquote(body.split("=")[1])
                if not url.startswith("http"):
                    url = "http://" + url

                if url not in self.urlList:
                    self.counter = self.counter + 1
                    conversion = "http://" + host + "/" + str(self.counter)
                    self.urlList.append(url)
                    self.conversions[conversion] = url
                    httpBody = ("<html><body>You introduced: " + url + "<br>"
                                + "The abbreviation is: " + conversion
                                + "<meta http-equiv='Refresh' content='2;"
                                + "url=http://" + host + "'>"
                                + "</body></html>")
                else:
                    httpBody = ("<html><body><h3>Url already shortened</h3>"
                                + "<meta http-equiv='Refresh' content='2;"
                                + "url=http://" + host + "'></body></html>")
        else:
            httpCode = "405 Method Not Allowed"
            httpBody = ("<html><body><h3>405 Method " + verb
                        + " not allowed</h3></body></html>")

        return (httpCode, httpBody)

if __name__ == '__main__':
    try:
        testshort = Shortener("localhost", 1234)
    except KeyboardInterrupt:
        print "\nFinished service"
        sys.exit()
