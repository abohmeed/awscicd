import boto3
import os


def lambda_handler(event, context):
    client = boto3.client('codecommit')
    client.post_comment_for_pull_request(
        pullRequestId=event['detail']['pullRequestId'],
        repositoryName=event['detail']['repositoryNames'][0],
        beforeCommitId=event['detail']['sourceCommit'],
        afterCommitId=event['detail']['destinationCommit'],
        content='A Pull Request was raised or changed. QA is runnig now and the results will appear here'
    )
    #     Start the build process
    client = boto3.client('codebuild')
    client.start_build(
        projectName=os.getenv("cb_project"),
        sourceVersion=event['detail']['sourceReference']
    )
