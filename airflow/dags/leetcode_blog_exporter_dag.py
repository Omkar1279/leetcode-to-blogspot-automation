from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from leetcode_scraper.leetcode_scraper import LeetCodeScraper
from blogspot_publisher.blogspot_publisher import BlogspotPublisher

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Function to scrape LeetCode submissions and publish them to Blogspot
def scrape_and_publish():
    # Initialize the scraper and log in
    scraper = LeetCodeScraper()
    scraper.login()
    # Fetch submissions
    submissions = scraper.fetch_submissions()
    # Initialize the publisher and publish the submissions
    publisher = BlogspotPublisher()
    publisher.publish_submissions(submissions)

# Define the DAG
with DAG(
    dag_id="leetcode_to_blogspot",
    default_args=default_args,
    description='Scrape LeetCode submissions and publish to Blogspot',
    schedule_interval=timedelta(days=1),  # Adjust as needed
    catchup=False,  # Prevent backfilling
) as dag:

    # Define the task using PythonOperator
    run_task = PythonOperator(
        task_id='scrape_and_publish',
        python_callable=scrape_and_publish,
    )

    # You can add more tasks and set their dependencies here if needed
    # For now, we just have one task
    run_task
