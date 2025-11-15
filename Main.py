import sys
import tkinter
from src.URL import URL
from src.Browser import Browser

browser = Browser()

if __name__ == "__main__":
    browser.load(URL(sys.argv[1]))
    tkinter.mainloop()