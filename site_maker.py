# -*- coding: utf-8 -*-
import markdown
import json
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
import os
from livereload import Server


env = Environment(loader=FileSystemLoader('./templates/'),
                  autoescape=True,
                  trim_blocks=False)


def markdowh_to_html(mdfile):
    with open(mdfile, 'r', encoding='utf-8') as md_file:
        html = markdown.markdown(md_file.read(), extension='codehilite')
        return html


def read_config():
    with open('./config.json', 'r', encoding='utf-8') as file:
        return json.loads(file.read())


def create_encyclopedia_pages(config, env):
    for item in config['articles']:
        html_file_name = (item['source'].split('/')[1].replace('md', 'html'))
        md_to_html = markdowh_to_html('articles/{}'.format(item['source']))
        template = env.get_template('page.html')
        with open('./{}'.format(html_file_name),
                  'w',
                  encoding='utf-8'
                  ) as html_file:
            html_file.write(template.render(
                md_to_html=md_to_html,
                title=item['title']))


def get_data_from_config(config):
    en_names = []
    for article in config['articles']:
        en_names.append((article['source'].split('/')[1].replace('md', 'html'),
                         article['title']))
    return en_names


def make_site():
    config = read_config()
    en_names = get_data_from_config(config)
    template = env.get_template('index.html')
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(template.render(navigation=en_names,
                                   topics=config['topics'],
                                   articles=config['articles'])
                   )
    create_encyclopedia_pages(config, env)


if __name__ == '__main__':
    config = read_config()
    # en_names = get_data_from_config(config)
    #create_encyclopedia_pages(config, env)
    make_site()
    server = Server()
    server.watch('articles/', make_site)
    server.watch('templates/', make_site)
    server.serve(root='./', debug=True)
    # for article in config['articles']:
    #     #print(article['source'])
    #     server.watch('articles/{}'.format(article['source']), make_site)
    # #server.watch('./templates/', make_site(en_names, config, env))
    #     server.serve(root='site/', debug=True)  # folder to serve html files from
