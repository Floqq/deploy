# Deployment program for Floqq's GAE Apps

Provides several programs to make the deployment procedure easier and more secure.

## Installation

    :::sh
    python setup.py install

## Run tests

    :::sh
    python setup.py test

## Development

    :::sh
    python setup.py develop

## Usage

The main commands are these:

    :::sh
    cd <app engine application to deploy directory>/
    floqq init
    floqq config <app name>.settings_url <path to settings>
    floqq deploy <git tree> <app name> <app version>

`<path to settings>` use app [settings](https://github.com/Floqq/settings)

`floqq deploy` is equivalent to running these commands in order:

    :::sh
    floqq-export
    floqq-prepare
    floqq-upload

`floqq-prepare` is equivalent to running these commands in order:

    :::sh
    floqq-fetch-settings
    floqq-unpack
    floqq-apply-settings
    floqq-decrypt-settings
    floqq-compilemessages
    floqq-dist

## Other commands

* `floqq-encrypt-settings`
* `floqq-deploy`
* `floqq-init`
* `floqq-config`

## Getting help

Run `command -h` for more help.
