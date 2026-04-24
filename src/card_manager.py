import json
import os

DATA_FILE = "flashcards.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"decks": [], "cards": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_card(front, back, deck):
    data = load_data()
    data["cards"].append({
        "front": front,
        "back": back,
        "deck": deck
    })

    if deck not in data["decks"]:
        data["decks"].append(deck)

    save_data(data)


def get_cards(deck=None):
    data = load_data()
    if deck:
        return [c for c in data["cards"] if c["deck"] == deck]
    return data["cards"]


def update_card(index, new_front, new_back, new_deck):
    data = load_data()
    data["cards"][index]["front"] = new_front
    data["cards"][index]["back"] = new_back
    data["cards"][index]["deck"] = new_deck

    if new_deck not in data["decks"]:
        data["decks"].append(new_deck)

    save_data(data)


def delete_card(index):
    data = load_data()
    data["cards"].pop(index)
    save_data(data)
