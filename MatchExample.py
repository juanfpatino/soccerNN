class MatchExample:
    def __init__(self, features, label, name):
        self.features: list = features  # list of attributes (floats)
        self.result: [] = label  # 0 if home win
        # 1 if away win
        # 2 if draw
        # 3 if no bet (upset)
        self.name: str = name

    def getFeatures(self):
        return self.features

    def getLabel(self):

        return self.result

    def __str__(self):

        if self.result == 0:
            res = "Home win"
        elif self.result == 1:
            res = "Draw"
        elif self.result == 2:
            res = "Away win"
        else:
            res = "No bet"

        return self.name + " | Label: " + res
