import logging
from typing import Generator

from plugin.connector.base import JiraBaseConnector

_LOGGER = logging.getLogger("spaceone")


class ProjectConnector(JiraBaseConnector):
    cloud_service_type = "Project"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_projects(self, secret_data: dict) -> list:
        params = {
            "maxResults": 3,
        }

        return self.dispatch_request(
            "GET", "rest/api/3/project/search", secret_data, params=params
        )

    def get_project(self, secret_data: dict, project_id_or_key: str) -> dict:
        params = {
            "expand": ["description", "lead", "issueTypes", "insight"],
            "fields": ["-customfield"],
        }

        response = self.dispatch_request(
            "GET", f"rest/api/3/project/{project_id_or_key}", secret_data, params=params
        )
        return next(response)

    def get_project_total_issue_count(
        self, secret_data: dict, project_id_or_key: str
    ) -> int:
        params = {"jql": f"project = '{project_id_or_key}'", "fields": ["-all"]}

        responses = self.dispatch_request(
            "GET", "rest/api/3/search", secret_data, params=params
        )

        return next(responses).get("total", 0)

    def search_issue(
        self,
        secret_data: dict,
        project_name: str,
    ) -> list:
        params = {
            "jql": f"project = '{project_name}'",
            "startAt": 0,
            "maxResults": 1,
            "fields": [
                "description",
                "summary",
                "comment",
                "created",
                "creator",
                "assignee",
                "duedate",
                "issuelinks",
                "issuetype",
                "labels",
                "lastViewed",
                "priority",
                "progress",
                "project",
                "reporter",
                "resolution",
                "resolutiondate",
                "status",
                "statuscategorychangedate",
                "subtasks",
                "updated",
                "watches",
            ],
        }
        request_url = "rest/api/3/search"
        _LOGGER.debug(f"[search_issue] {request_url}")

        responses = self.dispatch_request(
            "GET", request_url, secret_data, params=params
        )

        return responses
