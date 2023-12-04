class Player:
    def __init__(self, name):
        self.name = name 
        self.answer = ""
        self.db_id = 0
    
    def to_obj(self):
        obj = {
                "name": self.name,
                "answer": self.answer,
                "db_id": self.db_id
                }
        return obj
