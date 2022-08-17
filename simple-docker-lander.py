from bottle import route, run, template
import os
import yaml


DEFAULT_CONFIG = {
    'site-name': 'simple-docker-lander',
    'link-mode': 'default',
    'links': [
        {'name': 'Service 1', 'href': 'https://www.google.com/'},
        {'name': 'Service 2', 'href': 'https://www.reddit.com/'},
        {'name': 'Twitter', 'href': 'https://www.twitter.com/', 'group': 'Social Networks'},
        {'name': 'Facebook', 'href': 'https://www.facebook.com/', 'group': 'Social Networks'}
    ]
}


if __name__ == '__main__':
    config_env_var = yaml.safe_load(os.environ.get('CONFIG', '')) or {}

    # Merge the default config with the env config
    config = DEFAULT_CONFIG.copy()
    config.update(config_env_var)

    groups = [
        {'name': 'default', 'links': []}
    ]
    groups_index_map = {'default': 0}
    for link in config['links']:
        if 'group' in link:
            if link['group'] in groups_index_map:
                groups[groups_index_map[link['group']]]['links'].append(link)
            else:
                groups_index_map[link['group']] = len(groups)
                groups.append({
                    'name': link['group'],
                    'links': [link]
                })
        else:
            groups[0]['links'].append(link)

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
                margin: 0;
            }
            body > ul {
                padding: 0;
            }
            .group-name {
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        % if len(groups[0]['links']) > 0:
            <ul>
                % for link in groups[0]['links']:
                    <li><a href="{{ link['href'] }}"{{!' target="_blank"' if config['link-mode'] == 'tab' else ""}}>{{ link['name'] }}</a></li>
                % end
            </ul>
            <br />
        % end

        % for group in groups[1:]:
            <div class="group">
                <span class="group-name">{{ group['name'] }}</span>
                <ul>
                    % for link in group['links']:
                        <li><a href="{{ link['href'] }}"{{!' target="_blank"' if config['link-mode'] == 'tab' else ""}}>{{ link['name'] }}</a></li>
                    % end
                </ul>
            </div>
            <br />
        % end
    </body>
</html>''', config=config, groups=groups)

    kwargs = {
        'server': 'gunicorn',
        'host': '0.0.0.0',
        'port': '80',
        'workers': 10,
    }
    if 'SSL_KEYFILE' in os.environ:
        kwargs['keyfile'] = os.environ['SSL_KEYFILE']
    if 'SSL_CERTFILE' in os.environ:
        kwargs['certfile'] = os.environ['SSL_CERTFILE']
    if 'WORKERS' in os.environ:
        kwargs['workers'] = int(os.environ['WORKERS'])

    run(**kwargs)
