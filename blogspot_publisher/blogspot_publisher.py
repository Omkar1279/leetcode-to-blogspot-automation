from typing import List, Dict
from leetcode_scraper.data_models import LeetCodeSubmission
from googleapiclient.discovery import build
from collections import defaultdict
from config import config


class BlogspotPublisher:
    def __init__(self):
        self.api_key = config.BLOGSPOT_API_KEY
        self.blog_id = config.BLOG_ID
        self.service = build('blogger', 'v3', developerKey=self.api_key)

    def create_post(self, title: str, content: str):
        post = {
            "kind": "blogger#post",
            "title": title,
            "content": content
        }
        self.service.posts().insert(blogId=self.blog_id, body=post).execute()

    def organize_submissions(self, submissions: List[LeetCodeSubmission]) -> Dict:
        organized_data = defaultdict(lambda: defaultdict(list))
        for submission in submissions:
            year = submission.submission_date.year
            month = submission.submission_date.strftime('%B')
            organized_data[year][month].append(submission)
        return organized_data

    def generate_content(self, organized_data: Dict) -> str:
        content = ""
        for year, months in sorted(organized_data.items(), reverse=True):
            content += f"<details>\n<summary>{year}</summary>\n"
            for month, submissions in sorted(months.items(), reverse=True):
                content += f"<details>\n<summary>{month} ({len(submissions)})</summary>\n<ul>\n"
                for submission in submissions:
                    content += f"<li><a href='{submission.url}' target='_blank'>{submission.title}</a></li>\n"
                content += "</ul>\n</details>\n"
            content += "</details>\n"
        return content

    def generate_tagged_content(self, organized_data: Dict) -> str:
        tag_map = defaultdict(list)
        for year, months in organized_data.items():
            for month, submissions in months.items():
                for submission in submissions:
                    # Assuming tags are part of the submission data, you may need to modify this as necessary
                    tags = submission.tags
                    for tag in tags:
                        tag_map[tag].append(submission)

        content = ""
        for tag, submissions in sorted(tag_map.items()):
            content += f"<details>\n<summary>{tag} ({len(submissions)})</summary>\n<ul>\n"
            for submission in submissions:
                content += f"<li><a href='{submission.url}' target='_blank'>{submission.title}</a> - {submission.submission_date.strftime('%Y-%m-%d')}</li>\n"
            content += "</ul>\n</details>\n"
        return content

    def publish_submissions(self, submissions: List[LeetCodeSubmission]):
        organized_data = self.organize_submissions(submissions)
        sorted_content = self.generate_content(organized_data)
        tagged_content = self.generate_tagged_content(organized_data)

        self.create_post("LeetCode Solutions - Sorted by Date", sorted_content)
        self.create_post("LeetCode Solutions - Sorted by Tag", tagged_content)
