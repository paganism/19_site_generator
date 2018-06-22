import markdown
import json
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
import os
from livereload import Server

env = Environment(loader=FileSystemLoader('./templates/'),
                  autoescape=True,
                  trim_blocks=False)


def markdown_to_html(mdfile):
    with open(mdfile, 'r', encoding='utf-8') as md_file:
        html = markdown.markdown(md_file.read(), extension='codehilite')
        return html


def read_config():
    with open('./config.json', 'r', encoding='utf-8') as file:
        return json.loads(file.read())


def get_splitted_names(full_path_name):
    return full_path_name.split('/')[1].replace('md', 'html')


def create_encyclopedia_pages(config, env):
    for article in config['articles']:
        html_file_name = get_splitted_names(article['source'])
        md_to_html = markdown_to_html(os.path.join('articles/', article['source']))
        template = env.get_template('page.html')
        with open('static/{}'.format(html_file_name),
                  'w',
                  encoding='utf-8'
                  ) as html_file:
            html_file.write(template.render(
                md_to_html=md_to_html,
                title=article['title']))


def get_data_from_config(config):
    en_names = []
    for article in config['articles']:
        en_names.append((get_splitted_names(article['source']),
                         article['title']))
    return en_names


def make_site():
    config = read_config()
    en_names = get_data_from_config(config)
    create_encyclopedia_pages(config, env)
    template = env.get_template('index.html')
    with open('static/index.html', 'w', encoding='utf-8') as file:
        file.write(template.render(navigation=en_names,
                                   topics=config['topics'],
                                   articles=config['articles'])
                   )


if __name__ == '__main__':
    config = read_config()
    make_site()
    server = Server()
    server.watch('articles/', make_site)
    server.watch('templates/', make_site)
    server.serve(root='static/', debug=True)
