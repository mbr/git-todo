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
    obj['db'] = TODOBranch(repo, 'refs/heads/' + todo_branch)


@cli.command()
@click.option('--force', '-f',
              is_flag=True,
              help='Create new branch even if one exists')
@click.pass_obj
def new(obj, force):
    db = obj['db']
    gitconfig = obj['gitconfig']

    if db.exists and not force:
        click.echo('Branch {} already exists. Use --force to overwrite'
                   .format(obj['todo_branch']),
                   err=True)
        return sys.exit(1)

    name, email = gitconfig.get('user', 'name'), gitconfig.get('user', 'email')
    db.init_ref(name, email)
    click.echo('Created new branch \'{}\''.format(obj['todo_branch']))
