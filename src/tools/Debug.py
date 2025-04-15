


class Debug:
    @staticmethod
    def Log(text):
        print(f"\033[94m{text}\033[94m")
    @staticmethod
    def Error(text):
        print(f"\033[91m{text}\033[0m")