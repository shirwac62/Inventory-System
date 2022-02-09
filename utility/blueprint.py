from flask import Blueprint


class ProjectBlueprint(Blueprint):
    def __init__(self, blueprint, name):
        super().__init__(blueprint, name, template_folder='templates')

    @property
    def render(self):
        return {
            "title": self.title,
            "url": self.url,
            "blueprint": self.blueprint,
        }

    @property
    def title(self):
        return self.name.replace("_", " ").title()

    @property
    def url(self):
        return '/' + self.name.replace("_", "-")

    @property
    def blueprint(self):
        return self.name.replace(" ", "_").lower()

    def __repr__(self):
        return self.blueprint
