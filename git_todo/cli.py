import os
import sys

import click
from dulwich.repo import Repo

from .todo import TODOBranch


@click.group(invoke_without_command=True)
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
    obj['gitconfig'] = gitconfig = repo.get_config_stack()
    obj['db'] = TODOBranch(repo, 'refs/heads/' + todo_branch)
    obj['user_name'] = gitconfig.get('user', 'name')
    obj['user_email'] = gitconfig.get('user', 'email')

    if ctx.invoked_subcommand is None:
        return ctx.invoke(list_todos)


@cli.command()
@click.option('--force', '-f',
              is_flag=True,
              help='Create new branch even if one exists')
@click.pass_obj
def new(obj, force):
    db = obj['db']

    if db.exists and not force:
        click.echo('Branch {} already exists. Use --force to overwrite'
                   .format(obj['todo_branch']),
                   err=True)
        return sys.exit(1)

    name, email = obj['user_name'], obj['user_email']
    db.init_ref(name, email)
    click.echo('Created new branch \'{}\''.format(obj['todo_branch']))


@cli.command()
@click.pass_obj
def edit(obj):
    new_todo = click.edit(obj['db'].get_todo())
    name, email = obj['user_name'], obj['user_email']

    if new_todo is None:
        click.echo('No changes.')
    else:
        obj['db'].save_todo(name, email, new_todo)


@cli.command('list')
@click.pass_obj
def list_todos(obj):
    click.echo(obj['db'].get_todo(), nl=False)
