import tkinter.font
from abc import ABC, abstractmethod

from src.domain.layout.TextStyle import TextStyle


class TextMeasurer(ABC):
    @abstractmethod
    def measure(self, text: str, style: TextStyle) -> int:
        pass

    @abstractmethod
    def get_font(self, style: TextStyle) -> tkinter.font.Font:
        pass