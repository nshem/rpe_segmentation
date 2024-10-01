import jinja2

env = jinja2.Environment(loader=jinja2.FileSystemLoader('src/gui/templates/'))
template = env.get_template('home.html.jinja2')
    
def render(upload_callback: any, image_data: str) -> str:
    return template.render(upload_callback=upload_callback, image_data=image_data)