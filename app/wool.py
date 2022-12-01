class Wool:

    isAvailable = True
    needleGauge = "someAmmount"
    name = "SomeWool"
    price = 0.0
    composition = "100% Wool"
    brand = "SomeBrand"

    def __init__(self, name):
        self.name = name

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)
