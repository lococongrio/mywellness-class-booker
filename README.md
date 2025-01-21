# README

This is an automated script to sign up for classes of interest hosted by [MyWellness](https://www.mywellness.com/?language=nl), or any of its derivative gyms. The advantage is that it takes into account class booking opening hours, and does a short burst (5+5 seconds x 10 signups/second) of signup attempts just around the opening, so that you're nearly guaranteed a spot.

# Preferences

You can declare your preferences in `config.py`:
- `facilityId`:         The building you want to search lessons in, *mandatory*
- `matchers`:           A list of matchers for classes, based on a number of attributes
    - `eventTypeId`:    The type of class, *mandatory*
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

Some adjustments may need to be made in code with regards to:
- timezones (now set to CET)
- booking opening hours (now set to 20:00).

# To do

- [ ] Externalize
    - [ ] `x-mwapps-*` headers
    - [ ] timezone
    - [ ] burst trigger time
    - [ ] max sleep duration
- [ ] Merge `credentials.py` and `config.py` into `application-context.py`
- [ ] Generalize ClassEventMatchers
    - [ ] Make `eventTypeId` optional
    - [ ] Add event name as optional matcher