class Medicine:
    def __init__(self, name, quantity, price, description="Опис відсутній"):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.description = description


    def __str__(self):
        return f"{self.name} - Кількість: {self.quantity}, Ціна: {self.price}"
