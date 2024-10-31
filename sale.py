class Sales:
    def __init__(self, id, amount):
        self.id = id
        self.amount = amount

    def display(self):
        print(self.id, self.amount)