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
        if self.ref_name not in self.repo.refs:
            author = '{} <{}>'.format(author_name, author_email).encode('utf8')

            # create TODO branch
            blob = Blob.from_string(b'')
            tree = Tree()
            tree.add(b'TODO', 0o100644, blob.id)

            commit = Commit()
            commit.tree = tree.id
            commit.message = 'Initial commit for TODO branch'
            commit.encoding = 'UTF-8'

            tz = arrow.now().utcoffset().seconds
            commit.author = commit.committer = author
            commit.author_time = commit.commit_time = int(time())
            commit.commit_timezone = commit.author_timezone = tz

            # add objects to repo
            store = self.repo.object_store
            store.add_object(blob)
            store.add_object(tree)
            store.add_object(commit)

            # set branch
            self.repo.refs[self.ref_name] = commit.id
            return True
        return False

    def get_todo(self):
        commit = self.repo[self.repo.refs[self.ref_name]]
        tree = self.repo[commit.tree]
        mode, hash = tree.lookup_path(self.repo.__getitem__, 'TODO')
        blob = self.repo[hash]

        return blob.as_raw_string()
