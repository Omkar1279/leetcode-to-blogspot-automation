from blogspot_publisher.blogspot_publisher import BlogspotPublisher
from leetcode_scraper.leetcode_scraper import LeetCodeScraper

scraper = LeetCodeScraper()
scraper.login()
submissions = scraper.fetch_submissions()

publisher = BlogspotPublisher()
publisher.publish_submissions(submissions)
