# -*- coding: utf-8 -*-

# System
import os

# Third party
import click
from plumbum import ProcessExecutionError
from plumbum.cmd import python

LOCATION = os.path.dirname(os.path.abspath(__file__))

__version__ = '1.0'


def _user_loaddata():
    """ load dummy users """
    cmd = python[
        'manage.py',
        'loaddata',
        '{0}/users.json'.format(LOCATION)]
    cmd.run_fg()


def _import_dummy_data():
    """ load dummy order/item data """
    cmd = python[
        'manage.py',
        'loaddata',
        '{0}/dummyorders.json'.format(LOCATION)]
    cmd.run_fg()


def success(msg):
    """ output a success message """
    click.secho(msg, fg='green')


def error(msg):
    """ output error message """
    click.secho(msg, fg='red')


class CatchAllExceptions(click.Group):
    """ Wrap click.Groups to catch exceptions """
    def __call__(self, *args, **kwargs):   # noqa: D102
        try:
            return self.main(*args, **kwargs)
        except ProcessExecutionError as exc:
            error(exc.stderr)
            exit()


@click.command(help='Dummy Data')
def dummydata():
    """ import dummy users """
    _user_loaddata()
    success('Dummy users added success')
    """ import dummy data """
    _import_dummy_data()
    success('Dummy data import success')


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


cli.add_command(dummydata)


if __name__ == '__main__':
    cli()
