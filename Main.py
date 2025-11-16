import tkinter
from src.domain.url.URL import URL
from src.Browser import Browser

browser = Browser()

if __name__ == "__main__":
    browser.load(URL("https://browser.engineering/graphics.html"))
    tkinter.mainloop()