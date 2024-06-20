# LeetCode Solutions Archive Exporter

This project exports your solved LeetCode questions to the "LeetCode Solutions Archive" blog on Blogspot, organized by date. The project uses web scraping to extract data from LeetCode and Apache Airflow to orchestrate the workflow.

## Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/leetcode_blog_exporter.git
    cd leetcode_blog_exporter
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file** in the root directory with the following content:
    ```env
    LEETCODE_USERNAME=your_leetcode_username
    LEETCODE_PASSWORD=your_leetcode_password
    BLOGSPOT_API_KEY=your_blogspot_api_key
    BLOG_ID=your_blog_id
    ```

5. **Initialize Airflow**:
    ```bash
    airflow db init
    airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
    ```

6. **Start Airflow Scheduler and Webserver**:
    ```bash
    airflow scheduler
    airflow webserver
    ```

7. **Access Airflow UI** at `http://localhost:8080` and trigger the `leetcode_blog_exporter` DAG.
