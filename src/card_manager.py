import json
import os

DATA_FILE = "flashcards.json"

# Loads flashcard data from the JSON file
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"decks": [], "cards": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Saves updated flashcard data back to the JSON file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)



#Adds a new flashcard to the system
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


# Returns all cards, or only cards from a specific deck
def get_cards(deck=None):
    data = load_data()
    if deck:
        return [c for c in data["cards"] if c["deck"] == deck]
    return data["cards"]


# Updates an existing card by index
def update_card(index, new_front, new_back, new_deck):
    data = load_data()
    data["cards"][index]["front"] = new_front
    data["cards"][index]["back"] = new_back
    data["cards"][index]["deck"] = new_deck

    if new_deck not in data["decks"]:
        data["decks"].append(new_deck)

    save_data(data)

# Deletes a card by index
def delete_card(index):
    data = load_data()
    data["cards"].pop(index)
    save_data(data)
# Returns a list of all deck names
def get_decks():
    data = load_data()
    return data["decks"]

# Adds a new deck if it doesn't already exist
def add_deck(deck_name):
    data = load_data()
    if deck_name not in data["decks"]:
        data["decks"].append(deck_name)
        save_data(data)

# Deletes a deck and all cards inside it
def delete_deck(deck_name):
    data = load_data()

    # Remove deck
    if deck_name in data["decks"]:
        data["decks"].remove(deck_name)

    # Remove cards belonging to that deck
    data["cards"] = [c for c in data["cards"] if c["deck"] != deck_name]

    save_data(data)
