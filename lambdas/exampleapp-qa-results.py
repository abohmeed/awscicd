import re

import boto3


def GetPRFromBuild(event):
    buildid = event['detail']['build-id']
    client = boto3.client('codebuild')
    response = client.batch_get_builds(
        ids=[buildid]
    )
    resolvedSourceVersion = response['builds'][0]['resolvedSourceVersion']
    repository = event['detail']['additional-information']['source']['location'].split("/")[-1]
    client = boto3.client('codecommit')
    pull_requests = client.list_pull_requests(
        repositoryName=repository,
        pullRequestStatus='OPEN'
    )
    for p in pull_requests['pullRequestIds']:
        pr = client.get_pull_request(pullRequestId=p)
        destinationCommit = pr['pullRequest']['pullRequestTargets'][0]['destinationCommit']
        if resolvedSourceVersion == destinationCommit:
            break
    return pr


def GetContent(event):
    client = boto3.client('codebuild')
    project_name = event['detail']['project-name']
    source_branch = event['detail']['additional-information']['source-version'].split("/")[-1]
    response = client.batch_get_projects(
        names=[project_name]
    )
    badge = response['projects'][0]['badge']['badgeRequestUrl']
    # Modify the badge to reflect the correct source branch. Otherwise it will display "Unknown"
    badge = re.sub(r'branch=.*$', "branch={}".format(source_branch), badge)
    for phase in event['detail']['additional-information']['phases']:
        if phase.get('phase-status') == 'FAILED':
            content = '![Failing]({0} "Failing") - See the [Logs]({1})'.format(badge, event['detail'][
                'additional-information']['logs']['deep-link'])
            break
        else:
            content = '![Passing]({0} "Passing") - See the [Logs]({1})'.format(badge, event['detail'][
                'additional-information']['logs']['deep-link'])
    return content


def CommentOnPR(pr, content):
    client = boto3.client('codecommit')
    response = client.post_comment_for_pull_request(
        pullRequestId=pr['pullRequest']['pullRequestId'],
        repositoryName=pr['pullRequest']['pullRequestTargets'][0]['repositoryName'],
        beforeCommitId=pr['pullRequest']['pullRequestTargets'][0]['sourceCommit'],
        afterCommitId=pr['pullRequest']['pullRequestTargets'][0]['destinationCommit'],
        content=content
    )


def lambda_handler(event, context):
    pr = GetPRFromBuild(event)
    CommentOnPR(pr, GetContent(event))
