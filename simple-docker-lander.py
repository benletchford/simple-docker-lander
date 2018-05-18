from bottle import route, run, template
import os
import yaml


DEFAULT_CONFIG = {
    'site-name': 'simple-docker-lander',
    'link-mode': 'default',
    'links': [
        {'name': 'Example Site A', 'href': 'https://www.google.com.au/'},
        {'name': 'Example Site B', 'href': 'https://www.reddit.com/'}
    ]
}


if __name__ == '__main__':
    config_env_var = yaml.safe_load(os.environ.get('CONFIG', '')) or {}

    # Merge the default config with the env config
    config = DEFAULT_CONFIG.copy()
    config.update(config_env_var)

    @route('/')
    def index():
        return template('''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <title>{{ config['site-name'] }}</title>
    <style>
        ul {
            list-style-type: none;
            padding: 0;
            margin: 0;
        }
    </style>
  </head>
  <body>
    <ul>
      % for link in config['links']:
         <li><a href="{{ link['href'] }}"{{!' target="_blank"' if config['link-mode'] == 'tab' else ""}}>{{ link['name'] }}</a></li>
      % end
    </ul>
  </body>
</html>''', config=config)

    run(
        server='paste',
        host='0.0.0.0',
        port='80'
    )
