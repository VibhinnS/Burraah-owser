import sys
import tkinter
from src.domain.http.URL import URL
from src.adapters.parser.URLParser import URLParser
from src.ui.Browser import Browser

browser = Browser()

if __name__ == "__main__":
    while True:
        user_input = "http://www.example.org"
        if user_input:
            url: URL = URLParser.parse(user_input)
            browser.load(url)
            tkinter.mainloop()