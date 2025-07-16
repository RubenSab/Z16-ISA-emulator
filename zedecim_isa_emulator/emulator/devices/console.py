import readchar

class Console:
    def __init__(self):
        self.history = []

    def get_input(self):
        data = readchar.readchar()
        self.history.append(data + "\n")
        return data

    def output(self, data):
        self.history.append(data)
        print(data, end='')

    def export_history(self, filename):
        with open(filename, "w") as f:
            f.write(''.join(self.history))