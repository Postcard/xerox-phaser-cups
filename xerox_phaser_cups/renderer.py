from jinja2 import Environment, PackageLoader


JINJA_ENV = Environment(
    loader=PackageLoader('xerox_phaser_cups', 'templates')
)


def render(context):
    template = JINJA_ENV.get_template('a3_poster.html')
    return template.render(context)

