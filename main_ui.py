from tkinter import Frame, Tk, Canvas, Label, Button
from typing import cast


class MainUI(Frame):
    def __init__(self, master: Tk, ui):
        super().__init__(master)

        self.ui = ui
        self.canvas: Canvas = cast(Canvas, None)
        self.textCorrect: Label = cast(Label, None)
        self.textIncorrect: Label = cast(Label, None)

        self.configure_layout()
        self.create_top_bar()
        self.create_canvas()
        self.create_bottom_bar()

    def configure_layout(self) -> None:
        """Configure the main layout and the grid to be used"""
        self.grid_columnconfigure(tuple(range(9)), weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid(sticky="nsew", padx=10, pady=10)

        return None

    def create_top_bar(self) -> None:
        """Create the top navigation bar with the necessary buttons and separators"""
        topBar: Frame = Frame(self, bg="#e0e0e0", relief="raised", bd=1)
        topBar.grid(row=0, column=0, columnspan=9, sticky="ew", pady=(0, 10))
        topBar.grid_columnconfigure(tuple(range(9)), weight=1)

        buttonsStyles: dict = {
            "bg": "#4a7abc",
            "fg": "black",
            "font": ("Arial", 10, "bold"),
            "relief": "flat",
            "activebackground": "#3a5a8c",
            "padx": 10,
            "pady": 5,
            "borderwidth": 0,
            "cursor": "hand1"
        }

        timeBtnConfigs: list = [
            ("30s", "", 0),
            ("60s", "", 1),
            ("90s", "", 2),
            ("120s", "", 3)
        ]

        for time, command, col in timeBtnConfigs:
            btn = Button(topBar, text=time, **buttonsStyles)
            btn.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)
            setattr(self, f"btn{time}", btn)

        sep1: Frame = Frame(topBar, bg="#cccccc", width=2)
        sep1.grid(row=0, column=4, sticky="ns", padx=5)
        setattr(self, "separator1", sep1)

        extraBtnConfigs: list = [
            ("Specials", "", 5),
            ("Numbers", "", 6)
        ]

        for text, command, col in extraBtnConfigs:
            btn: Button = Button(topBar, text=text, **buttonsStyles)
            btn.grid(row=0, column=col, sticky="nsew", padx=2, pady=2)
            setattr(self, f"btn{text}", btn)

        sep2: Frame = Frame(topBar, bg="#cccccc", width=2)
        sep2.grid(row=0, column=7, sticky="ns", padx=5)
        setattr(self, f"separator2", sep2)

        profileStyle: dict = buttonsStyles.copy()
        profileStyle["bg"] = "#e74c3c"
        profileStyle["activebackground"] = "#c0392b"

        profile: Button = Button(topBar, text="Profile", command=self.switch_to_profile, **profileStyle)
        profile.grid(row=0, column=8, sticky="nsew", padx=2, pady=2)
        setattr(self, "btnProfile", profile)

        return None

    def create_canvas(self) -> None:
        """Create and configure the canvas to show the corresponding text"""
        canvasFrame: Frame = Frame(self, bg="#ffffff", bd=2, relief="ridge")
        canvasFrame.grid(row=1, column=0, columnspan=9, sticky="nsew", pady=5)
        canvasFrame.grid_columnconfigure(0, weight=1)
        canvasFrame.grid_rowconfigure(0, weight=1)

        self.canvas: Canvas = Canvas(canvasFrame, bg="#ffffff", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        return None

    def create_bottom_bar(self) -> None:
        """Create and configure the bottom bar to show few metrics"""
        statusBar: Frame = Frame(self, bg="#e0e0e0", relief="sunken", bd=1)
        statusBar.grid(row=2, column=0, columnspan=9, sticky="ew", pady=(10, 0))

        for i in range(0, 9):
            statusBar.grid_columnconfigure(i, weight=1)

        metricStyle: dict = {
            "font": ("Arial", 10, "normal"),
            "bg": "#e0e0e0",
            "padx": 10,
            "pady": 5
        }

        self.textCorrect: Label = Label(statusBar, text="Correct: 0", fg="#27ae60", anchor="w", **metricStyle)
        self.textCorrect.grid(row=0, column=0, columnspan=4, sticky="w")
        self.textIncorrect: Label = Label(statusBar, text="Incorrect: 0", fg="#c0392b", anchor="e", **metricStyle)
        self.textIncorrect.grid(row=0, column=4, columnspan=5, sticky="e")

        return None

    def switch_to_profile(self) -> None:
        """Switch to profile frame from the main frame"""
        self.ui.switch_frame(frameClassName="ProfileUI")
        return None
