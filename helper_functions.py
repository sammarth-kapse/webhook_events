import requests
import sys
from static_variables import *


def get_data_collection_from_github_api(url):
    data = []
    while 1:
        response = get_response_from_github_api(url)
        json_response = response.json()
        data += json_response
        if LINK in response.headers:
            url = get_next_page_url(response.headers[LINK])
        else:
            url = None

        if url is None:
            break

    return data


def get_next_page_url(links):
    links = links.split(", ")
    for link in links:
        ind = link.find('next')
        if ind != -1:
            return link[1:ind - 8]

    return None


def get_single_data_from_github_api(url):
    response = get_response_from_github_api(url)
    json_response = response.json()
    return json_response


def get_response_from_github_api(url):
    token = 'c1b10f829ce912233539e37dabc0e1fac7a516ca'
    headers = {'Authorization': 'token ' + token}

    response = requests.get(url, headers=headers)
    check_for_unexpected_response(response, url)

    return response


def check_for_unexpected_response(response, url):
    json_response = response.json()
    if MESSAGE in json_response:
        message = json_response[MESSAGE]
        if message.find(BAD_CREDENTIALS_MESSAGE) != -1:
            sys.exit(BAD_CREDENTIALS_MESSAGE)
        elif message.find(RATE_LIMIT_EXCEEDED_MESSAGE) != -1:
            sys.exit(RATE_LIMIT_EXCEEDED_MESSAGE)
        elif message.find(NOT_FOUND_MESSAGE) != -1:
            sys.exit(url + " is " + NOT_FOUND_MESSAGE)


def get_pr_reviewers(review_url):
    reviews_data = get_data_collection_from_github_api(review_url)
    unique_reviewers = set()
    for review in reviews_data:
        unique_reviewers.add(review[USER][LOGIN])
    reviewers = []
    for reviewer in unique_reviewers:
        user = {USER: reviewer}
        reviewers.append(user)
    return reviewers


def get_pr_commits(commits_url):
    commits_data = get_data_collection_from_github_api(commits_url)
    commits = []
    for commit_data in commits_data:
        commit = {SHA: commit_data[SHA], COMMITED_AT: commit_data[COMMIT][AUTHOR][DATE]}
        if commit_data[AUTHOR] is None:
            commit[AUTHOR] = commit_data[COMMIT][AUTHOR][NAME]
        else:
            commit[AUTHOR] = commit_data[AUTHOR][LOGIN]
        commits.append(commit)

    return commits


def get_pr_comments(pr_url):
    review_comments = get_review_comments(pr_url + "/" + REVIEWS)
    line_comments = get_line_comments(pr_url + "/" + COMMENTS)
    comments = review_comments + line_comments
    return comments


def get_review_comments(url):
    reviews = get_data_collection_from_github_api(url)

    review_comments = []
    for review in reviews:
        if review[BODY] and review[STATE] != PENDING:
            value = {USER: review[USER][LOGIN], BODY: review[BODY], SUBMITTED_AT: review[SUBMITTED_AT]}
            review_comments.append(value)

    return review_comments


def get_line_comments(url):
    comments = get_data_collection_from_github_api(url)
    line_comments = []
    for comment in comments:
        value = {USER: comment[USER][LOGIN], BODY: comment[BODY], SUBMITTED_AT: comment[UPDATED_AT]}
        line_comments.append(value)

    return line_comments


def get_changed_files(merge_commit_url):
    merge_commit_data = get_single_data_from_github_api(merge_commit_url)
    files_changed = []
    for file in merge_commit_data[FILES]:
        entry = {FILENAME: file[FILENAME], STATUS: file[STATUS], ADDITIONS: file[ADDITIONS], DELETIONS: file[DELETIONS]}
        files_changed.append(entry)

    return files_changed


def get_requested_reviewers(requested_reviewers):
    output = []
    for reviewer in requested_reviewers:
        user = {USER: reviewer[LOGIN]}
        output.append(user)
    return output


def get_merged_by(merged_by):
    if merged_by is None:
        return None
    else:
        return merged_by[LOGIN]
