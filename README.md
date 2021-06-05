# ShareX server made in Python with FastAPI.


## How to setup:
* Clone the repository wherever you want with ``git clone https://github.com/Taarek/sharex-server``.
* Install Poetry instructions can be found [here](https://python-poetry.org/docs/).
* Run ``poetry install`` in the cloned folder afterwards.

- If you don't want to install Poetry, install ``fastapi[all]`` and ``uvloop`` with pip.

    ⚠ ``uvloop`` is only installable on *nix systems, Windows is not supported, but you can still use this without uvloop. :)

* Configure the ``config.toml`` file to your liking.
* Configure the ``sharex_config.sxcu`` config file, specifically the ``RequestURL`` key.

After all that is done, you need to setup a reverse proxy that can also serve static content out of your specified folders in ``config.toml``, I personally recommend [Caddy](https://caddyserver.com/docs/quick-starts/static-files#caddyfile), but nginx works too. I do not recommend Apache though, for reasons...

After all that's done, you need to start the FastAPI app. There are some instructions [here](https://fastapi.tiangolo.com/deployment/manually/). I recommend using gunicorn with binding to uvicorn, instructed [here](https://www.uvicorn.org/deployment/#gunicorn)

### I also recommend using CloudFlare, to avoid your server IP getting leaked and their performance features is a nice bonus.