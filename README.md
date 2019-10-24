Playlist label
==============

A playlist label prototype running on a Raspberry Pi connected to a 12.3" screen.

## Run the development container

To run the development container:

`$ cd development` and `$ docker-compose up --build`

You should then be able to see the Flask server running at: http://localhost:8081

## Run tests locally

To run the python tests:

`$ cd development` and `$ docker-compose up --build` and `$ docker exec -it playlistlabel make linttest`

To run the javascript tests:

`$ cd testing` and `$ docker-compose up --build` and `$ docker exec -it javascripttests make linttestjs`

## Installation on Raspbian

To install and run on a Raspbian OS Raspberry Pi for prototyping:

* Install [Pyenv](http://www.knight-of-pi.org/pyenv-for-python-version-management-on-raspbian-stretch/) and Python 3.7.3
* Install the required packages `pip install -r requirements.txt`
* Copy `config.tmpl.env` to `source config.env` and fill in the relevant environment variables
* Run `source config.env`
* Run `./scripts/pi.sh`

## Installation via Balena

* Clone this repo.
* Add the Balena remote `git remote add balena g_acmi_developer@git.balena-cloud.com:g_acmi_developer/playlist-label-pi.git`
* Git push your changes
* Push your edits to Balena `git push balena master`

## Keyboard input from a shell

* Install xdotool `sudo apt install xdotool`
* To zoom out in the browser `xdotool key Ctrl+minus`
* To refresh the page `xdotool key "ctrl+F5"`
