import os
import sys

import click
from dulwich.repo import Repo

from .todo import TODOBranch


@click.group()
@click.option('--todo-branch', '-t', help='TODO branch name', default='todo')
@click.option('--repo', '-r', help='Path to git repo (default: auto)')
@click.pass_context
def cli(ctx, todo_branch, repo):
    ctx.obj = obj = {}
    obj['todo_branch'] = todo_branch

    if repo is None:
        # walk upwards until we find a .git path
        path = os.path.abspath(os.getcwd())

        while True:
            git_path = os.path.join(path, '.git')

            if os.path.exists(git_path) and os.path.isdir(git_path):
                repo = Repo(git_path)
                break

            path, tail = os.path.split(path)
            if not tail:
                break

    if repo is None:
        click.echo('No valid git repository found upwards of {}'
                   .format(os.getcwd()),
                   err=True)
        sys.exit(1)

    obj['repo'] = repo
    obj['gitconfig'] = repo.get_config_stack()


@cli.command()
@click.pass_obj
def new(obj):
    db = TODOBranch(obj['repo'], 'refs/heads/' + obj['todo_branch'])
    gitconfig = obj['gitconfig']

    name, email = gitconfig.get('user', 'name'), gitconfig.get('user', 'email')
    if db.init_branch(name, email):
        click.echo('Created new branch \'{}\''.format(obj['todo_branch']))
