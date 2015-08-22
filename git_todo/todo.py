from time import time

import arrow
from dulwich.objects import Blob, Tree, Commit


class TODOBranch(object):
    def __init__(self, repo, ref_name):
        self.repo = repo
        self.ref_name = ref_name

    @property
    def exists(self):
        return self.ref_name in self.repo.refs

    def init_ref(self, author_name, author_email):
        self.save_commit(
            *self.create_todo_commit(
                b'', 'Initial commit for TODO branch', author_name,
                author_email),
            update_ref=self.ref_name)

    def create_todo_commit(self, text, message, author_name, author_email,
                           parent_id=None):
        author = '{} <{}>'.format(author_name, author_email).encode('utf8')

        # create TODO branch
        blob = Blob.from_string(text.encode('utf8'))
        tree = Tree()
        tree.add(b'TODO', 0o100644, blob.id)

        commit = Commit()
        commit.tree = tree.id
        commit.message = message.encode('utf8')
        commit.encoding = 'UTF-8'

        if parent_id:
            commit.parents = [parent_id]

        tz = arrow.now().utcoffset().seconds
        commit.author = commit.committer = author
        commit.author_time = commit.commit_time = int(time())
        commit.commit_timezone = commit.author_timezone = tz

        # add objects to repo
        return commit, tree, blob

    def save_commit(self, commit, tree, blob, update_ref=None):
        store = self.repo.object_store
        store.add_object(blob)
        store.add_object(tree)
        store.add_object(commit)

        if update_ref:
            self.repo.refs[update_ref] = commit.id

    def get_todo(self):
        commit = self.repo[self.repo.refs[self.ref_name]]
        tree = self.repo[commit.tree]
        mode, hash = tree.lookup_path(self.repo.__getitem__, 'TODO')
        blob = self.repo[hash]

        return blob.as_raw_string().decode('utf8')

    def save_todo(self, author_name, author_email, content):
        self.save_commit(
            *self.create_todo_commit(
                content, 'Updated TODO', author_name, author_email,
                self.repo.refs[self.ref_name]),
            update_ref=self.ref_name)
