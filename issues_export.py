import requests
import json


class Issue(object):
    endpoint_schema = 'https://bitbucket.org/api/1.0/repositories/{accountname}/{repo_slug}/issues'

    def __init__(self, accountname, repo_slug, password):
        self.accountname = accountname
        self.repo_slug = repo_slug
        self.password = password
        self.endpoint = self.endpoint_schema.format({'accountname':accountname, 'repo_slug':repo_slug})

    def fetch(self):
        resp = requests.get(self.endpoint, auth=(self.accountname, self.password))
        return resp.json()


class Comment(object):
    endpoint_schema = 'https://bitbucket.org/api/1.0/repositories/{accountname}/{repo_slug}/issues/{issue_id}/comments'


def export_all(accountname, repo_slug, password):
    issue_obj = Issue(accountname=accountname, repo_slug=repo_slug, password=password)
    issues = issue_obj.fetch()
    for issue in issues:
        cmnt_obj = Comment(issue)
        issue['comments'] = cmnt_obj.fetch()
    return json.dumps(issues)


if __name__ == '__main__':
    import sys
    accountname = sys.argv[1]
    repo_slug = sys.argv[2]
    password = sys.argv[3]
    print export_all(accountname, repo_slug, password)
