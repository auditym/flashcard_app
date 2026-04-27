### Project Overview
This Flashcard App allows users to create, edit, delete, and study flashcards across multiple decks. It includes a clean GUI, dark mode, deck management, and persistent storage using JSON. The goal of the project is to provide a simple and effective study tool.

### Folder Structure
- src/
  - gui.py
  - card_manager.py
- data/
  - cards.json
- docs/
  - placeholder.txt
- VERSION.txt


2026-04-20 — 7 hours
- Added Study Mode screen
- Updated GUI to include Study Mode button
- Registered StudyModeScreen in main app
- Tested navigation and card flipping

2026-04-24 — 5 hours
- Added update_card and delete_card functions
- Implemented Edit/Delete buttons in ViewCardsScreen
- Added popup editor window for modifying cards
- Tested editing and deleting functionality


2026-04-24 — 6 hours
- Added DeckManagerScreen for managing decks
- Implemented add_deck and delete_deck functions
- Updated GUI navigation to include Deck Manager
- Tested deck creation and deletion

 2026-04-24 — 4 hours
- Integrated Deck Manager screen (add/delete decks)
- Added get_decks, add_deck, delete_deck functions in card_manager.py
- Updated GUI navigation to include Deck Manager
- Implemented Dark Mode toggle with global theme application
- Added apply_theme() to FlashcardApp for consistent styling
- Updated all screens to support theme switching
- Verified deck creation, deletion, and dark mode behavior across all screens
- 
2026-04-25 — 10
- Added descriptive comments across multiple functions for clarity
- Cleaned up formatting in gui.py by adding spacing for readability
- Added .gitignore file to prevent Python cache files from being tracked


