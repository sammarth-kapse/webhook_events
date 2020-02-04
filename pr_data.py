from helper_functions import *


def get_entities_from_webhook_data(webhook_data):
    if ACTION in webhook_data:
        output = {}
        if webhook_data[ACTION] == OPENED:
            output = get_tuple_for_opened_action(webhook_data[PULL_REQUEST], webhook_data[ACTION])
        elif webhook_data[ACTION] == CLOSED:
            output = get_tuple_for_closed_action(webhook_data[PULL_REQUEST], webhook_data[ACTION])
        elif webhook_data[ACTION] == REVIEW_REQUESTED:
            output = get_tuple_for_review_action(webhook_data[PULL_REQUEST], webhook_data[ACTION])
        else:
            output = None
        return output
    else:
        return "NO Data obtained"


def get_tuple_for_opened_action(pr_data, action):
    opened_tuple = {ACTION: action, REPO: pr_data[BASE][REPO][FULL_NAME], NUMBER: pr_data[NUMBER],
                    TITLE: pr_data[TITLE], ID: pr_data[ID], AUTHOR: pr_data[USER][LOGIN],
                    CREATED_AT: pr_data[CREATED_AT], NUMBER_OF_LINES_ADDED: pr_data[ADDITIONS],
                    NUMBER_OF_LINES_DELETED: pr_data[DELETIONS]}

    return opened_tuple


def get_tuple_for_closed_action(pr_data, action):
    closed_tuple = {ACTION: action, REPO: pr_data[BASE][REPO][FULL_NAME], NUMBER: pr_data[NUMBER],
                    TITLE: pr_data[TITLE], ID: pr_data[ID], AUTHOR: pr_data[USER][LOGIN],
                    CREATED_AT: pr_data[CREATED_AT], CLOSED_AT: pr_data[CLOSED_AT], MERGED_AT: pr_data[MERGED_AT],
                    NUMBER_OF_LINES_ADDED: pr_data[ADDITIONS], NUMBER_OF_LINES_DELETED: pr_data[DELETIONS],
                    MERGED_BY: get_merged_by(pr_data[MERGED_BY]),
                    FILES: get_changed_files(
                        BASE_URL + "/" + pr_data[BASE][REPO][FULL_NAME] + "/" + COMMITS + "/" + pr_data[
                            MERGE_COMMIT_SHA]),
                    COMMITS: get_pr_commits(pr_data[URL] + "/" + COMMITS), COMMENTS: get_pr_comments(pr_data[URL]),
                    REVIEWERS: get_pr_reviewers(pr_data[URL] + "/" + REVIEWS),
                    PENDING_REVIEWERS: get_requested_reviewers(pr_data[REQUESTED_REVIEWERS])}

    return closed_tuple


def get_tuple_for_review_action(pr_data, action):
    review_tuple = {ACTION: action, REPO: pr_data[BASE][REPO][FULL_NAME], NUMBER: pr_data[NUMBER],
                    TITLE: pr_data[TITLE], REQUESTED_REVIEWERS: get_requested_reviewers(pr_data[REQUESTED_REVIEWERS])}
    return review_tuple
