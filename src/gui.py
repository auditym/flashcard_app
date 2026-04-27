import tkinter as tk
from tkinter import ttk

from card_manager import (
    add_card,
    get_cards,
    update_card,
    delete_card,
    get_decks,
    add_deck,
    delete_deck,
)

from study_mode import StudySession


class FlashcardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flashcard Study App")
        self.geometry("500x500")

        # Dark mode state
        self.dark_mode = False

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (
            HomeScreen,
            CreateCardScreen,
            ViewCardsScreen,
            StudyModeScreen,
            DeckManagerScreen,
        ):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomeScreen)
        self.apply_theme()

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.apply_theme()

    def apply_theme(self):
        bg = "#1e1e1e" if self.dark_mode else "#ffffff"
        fg = "#ffffff" if self.dark_mode else "#000000"

        self.configure(bg=bg)
        self.container.configure(bg=bg)

        for frame in self.frames.values():
            frame.configure(bg=bg)
            for widget in frame.winfo_children():
                try:
                    widget.configure(bg=bg, fg=fg)
                except:
                    pass


class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Flashcard Study App", font=("Arial", 22)).pack(pady=20)

        ttk.Button(
            self,
            text="Create Card",
            command=lambda: controller.show_frame(CreateCardScreen),
        ).pack(pady=10)

        ttk.Button(
            self,
            text="View Cards",
            command=lambda: controller.show_frame(ViewCardsScreen),
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Study Mode",
            command=lambda: controller.show_frame(StudyModeScreen),
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Manage Decks",
            command=lambda: controller.show_frame(DeckManagerScreen),
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Toggle Dark Mode",
            command=self.toggle_dark_mode,
        ).pack(pady=10)

    def toggle_dark_mode(self):
        self.controller.dark_mode = not self.controller.dark_mode
        self.controller.apply_theme()


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
        ttk.Button(
            self, text="Back", command=lambda: controller.show_frame(HomeScreen)
        ).pack()

    def save_card(self):
        add_card(self.front_entry.get(), self.back_entry.get(), self.deck_entry.get())
        self.front_entry.delete(0, tk.END)
        self.back_entry.delete(0, tk.END)
        self.deck_entry.delete(0, tk.END)


class ViewCardsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="All Cards", font=("Arial", 18)).pack(pady=10)

        self.listbox = tk.Listbox(self, width=50)
        self.listbox.pack()

        ttk.Button(self, text="Refresh", command=self.load_cards).pack(pady=5)
        ttk.Button(self, text="Edit Selected", command=self.edit_selected).pack(pady=5)
        ttk.Button(self, text="Delete Selected", command=self.delete_selected).pack(
            pady=5
        )

        ttk.Button(
            self, text="Back", command=lambda: controller.show_frame(HomeScreen)
        ).pack(pady=10)

    def load_cards(self):
        self.listbox.delete(0, tk.END)
        self.cards = get_cards()
        for card in self.cards:
            self.listbox.insert(tk.END, f"{card['front']}  ->  {card['back']}")

    def get_selected_index(self):
        selection = self.listbox.curselection()
        if not selection:
            return None
        return selection[0]

    def edit_selected(self):
        index = self.get_selected_index()
        if index is None:
            return

        card = self.cards[index]

        popup = tk.Toplevel(self)
        popup.title("Edit Card")
        popup.geometry("300x250")

        tk.Label(popup, text="Front:").pack()
        front_entry = tk.Entry(popup)
        front_entry.insert(0, card["front"])
        front_entry.pack()

        tk.Label(popup, text="Back:").pack()
        back_entry = tk.Entry(popup)
        back_entry.insert(0, card["back"])
        back_entry.pack()

        tk.Label(popup, text="Deck:").pack()
        deck_entry = tk.Entry(popup)
        deck_entry.insert(0, card["deck"])
        deck_entry.pack()

        def save_changes():
            update_card(index, front_entry.get(), back_entry.get(), deck_entry.get())
            popup.destroy()
            self.load_cards()

        ttk.Button(popup, text="Save", command=save_changes).pack(pady=10)

    def delete_selected(self):
        index = self.get_selected_index()
        if index is None:
            return

        delete_card(index)
        self.load_cards()


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

        ttk.Button(
            self, text="Back", command=lambda: controller.show_frame(HomeScreen)
        ).pack(pady=10)

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


class DeckManagerScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Deck Manager", font=("Arial", 18)).pack(pady=10)

        self.listbox = tk.Listbox(self, width=40)
        self.listbox.pack()

        ttk.Button(self, text="Refresh", command=self.load_decks).pack(pady=5)
        ttk.Button(self, text="Add Deck", command=self.add_deck_popup).pack(pady=5)
        ttk.Button(self, text="Delete Selected", command=self.delete_selected).pack(
            pady=5
        )

        ttk.Button(
            self, text="Back", command=lambda: controller.show_frame(HomeScreen)
        ).pack(pady=10)

    def load_decks(self):
        self.listbox.delete(0, tk.END)
        decks = get_decks()
        for d in decks:
            self.listbox.insert(tk.END, d)

    def get_selected_deck(self):
        selection = self.listbox.curselection()
        if not selection:
            return None
        return self.listbox.get(selection[0])

    def add_deck_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Add Deck")
        popup.geometry("250x150")

        tk.Label(popup, text="Deck Name:").pack()
        entry = tk.Entry(popup)
        entry.pack()

        def save():
            add_deck(entry.get().strip())
            popup.destroy()
            self.load_decks()

        ttk.Button(popup, text="Save", command=save).pack(pady=10)

    def delete_selected(self):
        deck = self.get_selected_deck()
        if deck:
            delete_deck(deck)
            self.load_decks()

if __name__ == "__main__":
    app = FlashcardApp()
    app.mainloop()
