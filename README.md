# Deployment program for Floqq's GAE Apps

Provides several programs to make the deployment procedure easier and more secure.

## Installation

    python setup.py install

## Usage

The main commands are these:

    floqq init
    floqq config <app name>.settings_url <path to settings>
    floqq deploy <git tree> <app name> <app version>

Apart from those commands you have also:

* floqq-export
* floqq-upload
* floqq-prepare
* floqq-unpack
* floqq-fetch-settings
* floqq-apply-settings

Run `command -h` for more help.
