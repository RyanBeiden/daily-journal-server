class JournalEntry():
    
    def __init__(self, id, concept, entry, date, moodId):
        self.id = id
        self.concept = concept
        self.entry = entry
        self.date = date
        self.moodId = moodId
        self.mood = None
        self.tags = None
