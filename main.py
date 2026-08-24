notes = ["Letters in the alphabet : Twenty-six", "Python : An easy to learn programming language"]

def parse_notes(notes):
        flashcard = []
        for note in notes:
                colon_index = note.find(":")