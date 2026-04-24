import tkinter as tk
from tkinter import ttk

# Import your managers
from src.card_manager import add_card, get_cards
from src.study_mode import StudySession


class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flashcard Study App")
        self.geometry("500x400")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (HomeScreen, CreateCardScreen, ViewCardsScreen, StudyModeScreen):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomeScreen)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Flashcard Study App", font=("Arial", 20)).pack(pady=20)

        ttk.Button(self, text="Create Card",
                    command=lambda: controller.show_frame(CreateCardScreen)).pack(pady=10)

        ttk.Button(self, text="View Cards",
                    command=lambda: controller.show_frame(ViewCardsScreen)).pack(pady=10)

        #  Added Study Mode button
        ttk.Button(self, text="Study Mode",
                    command=lambda: controller.show_frame(StudyModeScreen)).pack(pady=10)


class CreateCardScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(self, text="Front:").pack()
        self.front_entry = tk.Entry(self)
        self.front_entry.pack()

        tk.Label(self, text="Back:").pack()
        self.back_entry = tk.Entry(self)
        self.back_entry.pack()

        tk.Label(self, text="Deck:").pack()
        self.deck_entry = tk.Entry(self)
        self.deck_entry.pack()

        ttk.Button(self, text="Save Card", command=self.save_card).pack(pady=10)
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(HomeScreen)).pack()

    def save_card(self):
        add_card(self.front_entry.get(), self.back_entry.get(), self.deck_entry.get())
        self.front_entry.delete(0, tk.END)
        self.back_entry.delete(0, tk.END)
        self.deck_entry.delete(0, tk.END)


class ViewCardsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(self, text="All Cards").pack(pady=10)

        self.listbox = tk.Listbox(self, width=50)
        self.listbox.pack()

        ttk.Button(self, text="Refresh", command=self.load_cards).pack(pady=10)
        ttk.Button(self, text="Back", command=lambda: controller.show_frame(HomeScreen)).pack()

    def load_cards(self):
        self.listbox.delete(0, tk.END)
        for card in get_cards():
            self.listbox.insert(tk.END, f"{card['front']}  ->  {card['back']}")


#  FULL Study Mode Screen (already integrated)
class StudyModeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Study Mode", font=("Arial", 18)).pack(pady=10)

        tk.Label(self, text="Choose Deck:").pack()
        self.deck_entry = tk.Entry(self)
        self.deck_entry.pack()

        ttk.Button(self, text="Start Session", command=self.start_session).pack(pady=10)

        self.card_label = tk.Label(self, text="", font=("Arial", 16), wraplength=400)
        self.card_label.pack(pady=20)

        ttk.Button(self, text="Flip", command=self.flip_card).pack(pady=5)
        ttk.Button(self, text="Next", command=self.next_card).pack(pady=5)
        ttk.Button(self, text="Previous", command=self.prev_card).pack(pady=5)
        ttk.Button(self, text="Shuffle", command=self.shuffle_cards).pack(pady=5)

        ttk.Button(self, text="Back", command=lambda: controller.show_frame(HomeScreen)).pack(pady=10)

        self.session = None

    def start_session(self):
        deck = self.deck_entry.get().strip()
        self.session = StudySession(deck if deck else None)
        self.update_card_display()

    def update_card_display(self):
        if not self.session or not self.session.cards:
            self.card_label.config(text="No cards found.")
            return

        card = self.session.current_card()
        text = card["front"] if self.session.showing_front else card["back"]
        self.card_label.config(text=text)

    def flip_card(self):
        if self.session:
            self.session.flip()
            self.update_card_display()

    def next_card(self):
        if self.session:
            self.session.next_card()
            self.update_card_display()

    def prev_card(self):
        if self.session:
            self.session.prev_card()
            self.update_card_display()

    def shuffle_cards(self):
        if self.session:
            self.session.shuffle()
            self.update_card_display()
