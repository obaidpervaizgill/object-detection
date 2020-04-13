import ssl

class context:
    def __init__(self):
        super().__init__()
        self.context = ssl._create_unverified_context()