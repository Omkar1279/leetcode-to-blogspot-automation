import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
from .data_models import LeetCodeSubmission
from config import config


class LeetCodeScraper:
    def __init__(self):
        self.username = config.LEETCODE_USERNAME
        self.password = config.LEETCODE_PASSWORD
        self.session = requests.Session()

    def login(self):
        try:
            login_url = "https://leetcode.com/accounts/login/"
            login_data = {
                "login": self.username,
                "password": self.password,
                "csrfmiddlewaretoken": self._get_csrf_token(login_url)
            }
            login_response = self.session.post(login_url, data=login_data)
            login_response.raise_for_status()  # Raise an HTTPError for bad responses
            if login_response.status_code == 200:
                print("Login successful!")
            else:
                print(f"Login failed with status code {login_response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during login: {e}")

    def fetch_submissions(self) -> List[LeetCodeSubmission]:
        submissions = []
        try:
            url = f"https://leetcode.com/{self.username}/submissions/"
            response = self.session.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')

            table = soup.find('table', class_='reactable-data')
            if table:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip the header row
                    cols = row.find_all('td')
                    if len(cols) >= 7:
                        submission_date_str = cols[1].text.strip()
                        submission_date = datetime.strptime(submission_date_str, '%Y-%m-%d %H:%M:%S')
                        problem_link = cols[2].find('a')['href']
                        problem_title = cols[2].text.strip()
                        submission_status = cols[5].text.strip()
                        submission = LeetCodeSubmission(title=problem_title, url=problem_link,
                                                        submission_date=submission_date,
                                                        status=submission_status)
                        submissions.append(submission)
                    else:
                        print(f"Unexpected row format: {cols}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during fetch_submissions: {e}")

        return submissions

    def _get_csrf_token(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})['value']
            return csrf_token
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during CSRF token retrieval: {e}")
            return None
