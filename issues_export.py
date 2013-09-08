import requests
import json


class Issue(object):
    endpoint_schema = 'https://bitbucket.org/api/1.0/repositories/{accountname}/{repo_slug}/issues'

    def __init__(self, accountname, repo_slug, password):
        self.accountname = accountname
        self.repo_slug = repo_slug
        self.password = password
        self.endpoint = self.endpoint_schema.format(**{'accountname': accountname, 'repo_slug': repo_slug})

    def fetch(self):
        resp = requests.get(self.endpoint, auth=(self.accountname, self.password))
        return resp.json()['issues']


class Comment(object):
    endpoint_schema = 'https://bitbucket.org/api/1.0/repositories/{accountname}/{repo_slug}/issues/{issue_id}/comments'

    def __init__(self, issue_obj):
        self.issue = issue_obj

    def fetch(self, issue_id):
        self.endpoint = self.endpoint_schema.format(**{'accountname': self.issue.accountname, 'repo_slug': self.issue.repo_slug,
                                                    'issue_id': issue_id})
        resp = requests.get(self.endpoint, auth=(self.issue.accountname, self.issue.password))
        return resp.json()


def export_all(accountname, repo_slug, password):
    issue_obj = Issue(accountname=accountname, repo_slug=repo_slug, password=password)
    issues = issue_obj.fetch()
    cmnt_obj = Comment(issue_obj)
    for issue in issues:
        issue['comments'] = cmnt_obj.fetch(issue['local_id'])
    return json.dumps(issues)


if __name__ == '__main__':
    import sys
    accountname = sys.argv[1]
    repo_slug = sys.argv[2]
    password = sys.argv[3]
    print export_all(accountname, repo_slug, password)
