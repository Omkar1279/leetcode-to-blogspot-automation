from leetcode_scraper.leetcode_scraper import LeetCodeScraper

scraper = LeetCodeScraper()
scraper.login()
submissions = scraper.fetch_submissions()

for submission in submissions:
    print(submission.title, submission.url, submission.submission_date, submission.status)
