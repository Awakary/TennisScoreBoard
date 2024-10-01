from jinja2 import Environment, FileSystemLoader

from utils import selected_matches


class Render:

    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates'))

    def render_template(self, file_name, render_objects=None, pagination=None):
        template = self.env.get_template(file_name)
        self.env.filters['selected_matches'] = selected_matches

        if file_name == 'matches.html':
            return template.render(matches=render_objects['matches'],
                                   players=render_objects['players'],
                                   pagination=pagination)
        if file_name == 'match_score.html':
            return template.render(match=render_objects)
        if file_name == 'error.html':
            return template.render(error=render_objects)
        return template.render()





