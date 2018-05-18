# simple-docker-lander

## What does this do?

It builds a very basic HTML landing page that contains links (passed in via an environment variable) and serves it.

## How Simple?

Very simple one file, 53 lines of Python.

## Usage

Designed to fit elegantly into a `docker-compose` file:

```
version: '3.1'
services:
  simple-docker-lander:
    benletchford/simple-docker-lander:latest
    restart: always
    ports:
      - 80:80
    environment:
      CONFIG: |
        site-name: my-awesome-site
        link-mode: tab
        links:
          - name: Service 1
            href: https://www.google.com.au/
          - name: Service 2
            href: https://reddit.com/
```

As you can see, just populate the `CONFIG` environment variable with a `YAML` string.

## Configuration

`site-name`: the `<title>` value of the HTML document.

`link-mode`: can be set to `tab` or omitted completely for default link behaviour. If `tab`, it adds `target="_blank"` to links.

`links`: a `YAML` array of items each containing both a `name` (link value) and `href` (link target).

## Docker Build

Build and run the docker image.
```
$ docker build -t simple-docker-lander .
$ docker run -it --rm -p 80:80 --name simple-docker-lander simple-docker-lander
```
