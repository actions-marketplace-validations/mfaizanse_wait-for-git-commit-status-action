import os
import time
import requests
import json
import logging
logging.basicConfig(level=logging.INFO)

def readInputs():
    githubToken = os.environ.get("GITHUB_TOKEN")
    repositoryOwner = os.environ.get("GITHUB_OWNER")
    repository = os.environ.get("GITHUB_REPO")

    context = os.environ.get("CONTEXT")
    commit_ref = os.environ.get("COMMIT_REF")
    timeout = os.environ.get("TIMEOUT") # milliseconds
    if timeout:
        try:
            timeout = int(timeout)
        except Exception:
            exit('ERROR: Input timeout is not an integer')
    else:
        timeout = 180

    return {
        "context": context,
        "commit_ref": commit_ref,
        "timeout": timeout,
        "githubToken": githubToken,
        "repositoryOwner": repositoryOwner,
        "repository": repository
    }

def printInputs(inputs):
    print('****Using the following configurations:****')
    print('Context : {}'.format(inputs['context']))
    print('Commit REF : {}'.format(inputs['commit_ref']))
    print('Timeout : {}'.format(inputs['timeout']))
    print('Owner : {}'.format(inputs['repositoryOwner']))
    print('Repository : {}'.format(inputs['repository']))

def fetchCommitStatuses(owner, repo, sha, githubToken):
    url = "https://api.github.com/repos/{}/{}/commits/{}/status".format(owner, repo, sha)
    reqHeaders = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'Authorization' : 'Bearer {}'.format(githubToken)
    }

    logging.info('Fetching commit status from {}'.format(url))
    response = requests.get(url, headers=reqHeaders)
    if response.status_code != 200:
        raise Exception('API call failed. Status code: {}, {}'.format(response.status_code, response.text))
    return response.json() 
    
def getCommitStatusByContext(context, statuses):
    for status in statuses:
        if context == status['context']:
            return status
    return None

def set_action_output(name, value):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'{name}={value}', file=fh)

def main():
    inputs = readInputs()
    printInputs(inputs)
    
    startTime = time.time() # seconds
    while True:
        if (time.time() - startTime)*1000 > inputs['timeout']:
            exit('Action timed out.')
        time.sleep(0.5)
        commitStatus = fetchCommitStatuses(inputs['repositoryOwner'], inputs['repository'], inputs['commit_ref'], inputs['githubToken'])
        status = getCommitStatusByContext(inputs['context'], commitStatus['statuses'])
        if status == None:
            logging.info('Status not found!')
            continue
        elif status['state'] == 'pending':
            logging.info('Status state: {}'.format(status['state']))
            continue
        elif status['state'] == 'failure':
            jsonStr = json.dumps(status)
            set_action_output('state', status['state'])
            set_action_output('json', jsonStr)
            print(status)
            exit(1)
        elif status['state'] == 'success':
            jsonStr = json.dumps(status)
            set_action_output('state', status['state'])
            set_action_output('json', jsonStr)
            print(status)
            exit(0)
        else:
            exit('Unknown status.state: {}'.format(status['state']))
    

if __name__ == "__main__":
    main()
