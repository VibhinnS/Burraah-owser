from src.domain.html.Text import Text
from src.domain.html.Tag import Tag
from src.domain.layout.Parameters import Parameters
from src.domain.layout.TextStyle import TextStyle

from src.ports.repositories.layout.LayoutRepository import TextMeasurer

class Layout:
    def __init__(self, measurer, tokens):
        self.display_list: list = []
        self.measurer: TextMeasurer = measurer
        self.line: list = []
        self.parameters = Parameters()

        for token in tokens:
            self.token(token)

        self.flush()

    def token(self, token):
        if isinstance(token, Text):
            self.handle_text(token)
        if isinstance(token, Tag):
            self.handle_tags(token)

    def handle_text(self, token : Text):
        for word in token.text.split():
            style = TextStyle(
                self.parameters.CHAR_SIZE,
                self.parameters.WEIGHT,
                self.parameters.STYLE
            )
            font = self.measurer.get_font(style)
            word_width = self.measurer.measure(
                word,
                style
            )

            if self.parameters.CURSOR_X + word_width > self.parameters.WIDTH - self.parameters.HSTEP:
                self.flush()
                self.parameters.CURSOR_Y += font.metrics("linespace")*1.25
                self.parameters.CURSOR_X = self.parameters.HSTEP

            self.line.append((self.parameters.CURSOR_X, word, font))
            self.parameters.CURSOR_X += word_width + font.measure(" ")

    def handle_tags(self, token: Tag):
        if token.tag == "i":
            self.parameters.STYLE = "italic"
        elif token.tag == "/i":
            self.parameters.STYLE = "roman"
        elif token.tag == "b":
            self.parameters.WEIGHT = "bold"
        elif token.tag == "/b":
            self.parameters.WEIGHT = "normal"
        elif token.tag == "small":
            self.parameters.CHAR_SIZE -= 2
        elif token.tag == "/small":
            self.parameters.CHAR_SIZE += 2
        elif token.tag == "big":
            self.parameters.CHAR_SIZE += 4
        elif token.tag == "/big":
            self.parameters.CHAR_SIZE -= 4
        elif token.tag == "br":
            self.flush()
        elif token.tag == "/p":
            self.flush()
            self.parameters.CURSOR_Y += self.parameters.VSTEP

    def flush(self):
        if not self.line: return
        metrics = [font.metrics() for x,word,font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.parameters.CURSOR_Y + 1.25 * max_ascent
        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x,y,word,font))

        max_descent = max(metric["descent"] for metric in metrics)
        self.parameters.CURSOR_Y = baseline + 1.25 * max_descent
        self.parameters.CURSOR_X = self.parameters.HSTEP
        self.line = []