class Category:
    def __init__(self, name):
        self.name = name
        self.scenes = []

    def addscene(self, scene):
        self.scenes.append(scene)

    def get_name(self):
        return self.name

    def get_scenes(self):
        return self.scenes
