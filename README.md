# README

This is an automated script to sign up for classes of interest hosted by [MyWellness](https://www.mywellness.com/?language=es), or any of its derivative gyms.
The advantage is that it takes into account  and does a short burst (5+5 seconds x 10 signups/second) of signup attempts just around the opening, so that you're nearly guaranteed a spot.

## Fork of https://github.com/mboogerd/mywellness by @mboogerd. Thanks to him for the awesome work!
Features added/adapted:
- Book events by name in config.yaml
- Event id optional
- Just trying to book the first event _(closest one)_ 24h + 5 seconds in advance _(my gym only allows me to book one event per day and 24h in advance)_
- App running inside docker container
- Env variables copied from .env.dist to .env and passed to docker container
- Download of events data _(commented by default)_
- Time and gym settings changed to Spain 😉

# Preferences

You can declare your preferences in `config.py`:
- `facilityId`:         The building you want to search lessons in, *mandatory*
- `matchers`:           A list of matchers for classes, based on a number of attributes
    - `eventName`:      The name of the class, *optional*
    - `eventTypeId`:    The type of class, *optional*
    - `day`:            The starting day (Monday=0, ..., Sunday=6) of the class, *optional*
    - `hour`:           The starting hour (24H format) of the class, *optional*

Note that these identifiers will have to be found yourself. You can do so by using your browsers debugging mode and looking for network calls towards mywellness.com, notably `Search` and `Book`.

# Authentication (& Authorization)

The script expects two environment variables to be set:
- `HWF_USERNAME` (should be an e-mail address)
- `HWF_PASSWORD`

# Installing

1. Fork this repository
2. Configure your own preferences
3. Setup the repository secrets for Authentication

# Running the application with docker
1. Run `make run` _(add your mywellness email/password to .env)_
