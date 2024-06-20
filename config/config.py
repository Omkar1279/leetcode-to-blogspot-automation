import os
from dotenv import load_dotenv

load_dotenv()

LEETCODE_USERNAME = os.getenv('LEETCODE_USERNAME')
LEETCODE_PASSWORD = os.getenv('LEETCODE_PASSWORD')
BLOGSPOT_API_KEY = os.getenv('BLOGSPOT_API_KEY')
BLOG_ID = os.getenv('BLOG_ID')


