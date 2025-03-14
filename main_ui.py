from tkinter import Frame, Tk, Canvas, Label, Button, Event
from threading import Thread
from random import choice
from typing import cast
import time


class MainUI(Frame):
    def __init__(self, master: Tk, ui):
        super().__init__(master)
        self.ui = ui
        self.canvas: Canvas = cast(Canvas, None)
        self.maxCanvasChars: int = 50
        self.textCorrect: Label = cast(Label, None)
        self.textIncorrect: Label = cast(Label, None)
        self.textTimer: Label = cast(Label, None)
        self.seconds: int = 0
        self.numbers: bool = False
        self.specials: bool = False
        self.test_on: bool = False
        self.timer_on: bool = False
        self.bindings: list = [
            ("<Return>", self.start_typing_test),
            ("<Escape>", self.finish_typing_test)
        ]
        self.bindIds: list = []
        self.words: list = []
        self.configure_layout()
        self.create_top_bar()
        self.create_canvas()
        self.create_bottom_bar()
        self.set_time_variable(30)

    def configure_layout(self) -> None:
        """Configure the main layout and the grid to be used"""
        self.config(bg=self.ui.styles.get("background_color"))
        self.grid_columnconfigure(tuple(range(9)), weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid(sticky="nsew", padx=10, pady=10)
        return None

    def on_frame_activation(self) -> None:
        """Set the frame's key bindings and save them for later use"""
        for bind, callback in self.bindings:
            bindId = self.master.bind(bind, callback)
            self.bindIds.append((bind, bindId))
        return None

    def on_frame_deactivation(self) -> None:
        """Unset the frame's key bindings and clear the list"""
        for seq, bId in self.bindIds:
            self.master.unbind(seq, bId)
        self.bindIds = []
        return None

    def create_top_bar(self) -> None:
        """Create the top navigation bar with the necessary buttons and separators"""
        topBar: Frame = Frame(self, bg=self.ui.styles.get("background_color"), relief="flat", bd=1)
        topBar.grid(row=0, column=0, columnspan=9, sticky="ew", pady=20)
        topBar.grid_columnconfigure(tuple(range(9)), weight=1)
        buttonsStyles: dict = {
            "bg": self.ui.styles.get("background_color"),
            "fg": self.ui.styles.get("button_font_color"),
            "font": self.ui.styles.get("button_font"),
            "relief": "flat",
            "activebackground": self.ui.styles.get("button_active_color"),
            "padx": 10,
            "pady": 5,
            "borderwidth": 0,
            "cursor": "center_ptr"
        }
        timeBtnConfigs: list = [
            ("30s", self.set_time_variable, 0, 30),
            ("60s", self.set_time_variable, 1, 60),
            ("90s", self.set_time_variable, 2, 90),
            ("120s", self.set_time_variable, 3, 120)
        ]
        for text, command, col, secs in timeBtnConfigs:
            btn: Button = Button(topBar, text=text, command=lambda t=secs, cmd=command: cmd(t), **buttonsStyles)
            btn.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)
            setattr(self, f"btn{text}", btn)
        sep1: Frame = Frame(topBar, bg=self.ui.styles.get("background_color"), width=2)
        sep1.grid(row=0, column=4, sticky="ns", padx=5)
        setattr(self, "separator1", sep1)
        extraBtnConfigs: list = [
            ("Specials", self.set_specials_variable, 5),
            ("Numbers", self.set_numbers_variable, 6)
        ]
        for text, command, col in extraBtnConfigs:
            btn: Button = Button(topBar, text=text, command=command, **buttonsStyles)
            btn.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)
            setattr(self, f"btn{text}", btn)
        sep2: Frame = Frame(topBar, bg=self.ui.styles.get("background_color"), width=2)
        sep2.grid(row=0, column=7, sticky="ns", padx=5)
        setattr(self, f"separator2", sep2)
        profile: Button = Button(topBar, text="Profile", command=self.switch_to_profile, **buttonsStyles)
        profile.grid(row=0, column=8, sticky="nsew", padx=2, pady=2)
        setattr(self, "btnProfile", profile)
        return None

    def create_canvas(self) -> None:
        """Create and configure the canvas to show the corresponding text"""
        canvasFrame: Frame = Frame(self, bg=self.ui.styles.get("background_color"), relief="sunken")
        canvasFrame.grid(row=1, column=0, columnspan=9, sticky="nsew", pady=20)
        canvasFrame.grid_columnconfigure(0, weight=1)
        canvasFrame.grid_rowconfigure(0, weight=1)
        self.canvas: Canvas = Canvas(canvasFrame, bg=self.ui.styles.get("canvas_color"), highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        return None

    def create_bottom_bar(self) -> None:
        """Create and configure the bottom bar to show few metrics"""
        statusBar: Frame = Frame(self, bg=self.ui.styles.get("background_color"), relief="flat", bd=1)
        statusBar.grid(row=2, column=0, columnspan=9, sticky="ew", pady=20)
        for i in range(0, 9):
            statusBar.grid_columnconfigure(i, weight=1)
        metricStyle: dict = {
            "font": self.ui.styles.get("button_font"),
            "bg": self.ui.styles.get("background_color"),
            "padx": 10,
            "pady": 20
        }
        self.textCorrect: Label = Label(statusBar, text="Correct: 0", fg="#27ae60", anchor="w", **metricStyle)
        self.textCorrect.grid(row=0, column=0, columnspan=3, sticky="w")
        self.textTimer: Label = Label(statusBar, text="Time: 0", fg="#000000", **metricStyle)
        self.textTimer.grid(row=0, column=3, columnspan=3, sticky="ns")
        self.textIncorrect: Label = Label(statusBar, text="Incorrect: 0", fg="#c0392b", anchor="e", **metricStyle)
        self.textIncorrect.grid(row=0, column=6, columnspan=3, sticky="e")
        return None

    def switch_to_profile(self) -> None:
        """Switch to profile frame from the main frame"""
        if not self.test_on:
            self.ui.switch_frame(frameClassName="ProfileUI")
        return None

    def set_time_variable(self, seconds: int) -> None:
        """Change the time used for the tests"""
        if not self.test_on:
            self.seconds = seconds
            self.textTimer.config(text=f"Time: {self.seconds}s")
        return None

    def set_numbers_variable(self) -> None:
        """Change the numbers variable to enable or disable them"""
        if not self.test_on:
            self.numbers = not self.numbers
            print(f"Numbers are {self.numbers}")
        return None

    def set_specials_variable(self) -> None:
        """Change the specials variable to enable or disable them"""
        if not self.test_on:
            self.specials = not self.specials
            print(f"Specials are {self.specials}")
        return None

    def start_timer(self) -> None:
        """Start the timer for the typing test"""
        self.timer_on = True

        def countdown() -> None:
            remainingTime: int = self.seconds
            while remainingTime > 0 and self.timer_on:
                time.sleep(1)
                remainingTime -= 1
                self.textTimer.config(text=f"Time: {remainingTime}s")
            if remainingTime <= 0:
                self.timer_on = False
            return None

        timerThread: Thread = Thread(target=countdown)
        timerThread.daemon = True
        timerThread.start()
        return None

    def start_typing_test(self, event: Event) -> None:
        """Start the typing test by setting variables and calling the appropriate functions"""
        if not self.test_on and not self.timer_on:
            print(f"Test started using {event.keysym} key.")
            self.test_on = True
            self.initialize_words_array(language="english")
            self.start_timer()
            self.typing_test()
        return None

    def finish_typing_test(self, event: Event) -> None:
        """Finish the typing test only if a typing test has been started and the timer has ended"""
        if self.test_on and not self.timer_on:
            print(f"Typing test finished using {event.keysym} key.")
            self.clear_test()
        return None

    def clear_test(self) -> None:
        """Clear and set the configurations to the initial ones in order to set ready the next test"""
        self.timer_on = False
        self.test_on = False
        self.textTimer.config(text=f"Time: {self.seconds}s")
        self.canvas.delete("all")
        return None

    def initialize_words_array(self, language: str) -> None:
        """Get all the words from the txt files corresponding to the received language and store them in a list"""
        with open(file=f"{language}_words.txt", mode="r") as file:
            self.words: list = [word.replace("\n", "") for word in file.readlines()]
        return None

    def get_random_word(self) -> str:
        """Return a random word from the initialized list of words"""
        return choice(self.words)

    def create_text_line(self) -> str:
        """Return a created line with the right amount of random words in order to be display in the canvas"""
        line: list = []
        totalLength: int = 0
        firstWord: str = self.get_random_word()
        line.append(firstWord)
        totalLength += len(firstWord)
        lastWord = firstWord
        while totalLength < self.maxCanvasChars:
            line.append(" ")
            totalLength += 1
            word = self.get_random_word()
            if word != lastWord:
                if (totalLength + len(word)) < self.maxCanvasChars:
                    line.append(word)
                    totalLength += len(word)
                    lastWord = word
                else:
                    pass
            else:
                line.pop()
        return "".join(line)

    def typing_test(self) -> None:
        """Initialize, create and check the typing test"""
        line1 = self.canvas.create_text(
            720, 120, text=self.create_text_line(), font=self.ui.styles.get("canvas_label_font"),
            fill=self.ui.styles.get("label_font_color")
        )
        line2 = self.canvas.create_text(
            720, 240, text=self.create_text_line(), font=self.ui.styles.get("canvas_label_font"),
            fill=self.ui.styles.get("label_font_color")
        )
        line3 = self.canvas.create_text(
            720, 360, text=self.create_text_line(), font=self.ui.styles.get("canvas_label_font"),
            fill=self.ui.styles.get("label_font_color")
        )
        line4 = self.canvas.create_text(
            720, 480, text=self.create_text_line(), font=self.ui.styles.get("canvas_label_font"),
            fill=self.ui.styles.get("label_font_color")
        )
        return None
