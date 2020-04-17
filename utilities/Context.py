import ssl


class Context:
    context = ssl._create_unverified_context()
