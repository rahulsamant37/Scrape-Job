import requests
import os
import csv
from time import sleep
from datetime import datetime
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

class CareerjetAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://public.api.careerjet.net/search"

    def search(self, params):
        try:
            params['api_key'] = self.api_key
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None

def fetch_jobs(cj, job_type, country):
    search_params = {
        'affid': 'cd918e610ecfbcd6cc50f9527541794c',
        'user_ip': '127.0.0.1',
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'url': 'http://www.example.com/jobsearch',
        'keywords': job_type,
        'location': country,
        'sort': 'date',
        'contracttype': 'p',
        'contractperiod': 'f',
        'page': 1
    }

    all_jobs = []
    while True:
        result = cj.search(search_params)
        if not result or 'jobs' not in result or not result['jobs']:
            break

        all_jobs.extend(result['jobs'])
        if 'pages' in result and search_params['page'] >= result['pages']:
            break

        search_params['page'] += 1
    return job_type, country, all_jobs

def save_jobs_to_csv(output_file, job_data):
    with open(output_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=job_data[0].keys())
        writer.writerows(job_data)

def main():
    # Clear proxy settings
    os.environ.pop('http_proxy', None)
    os.environ.pop('https_proxy', None)

    # Initialize client
    cj = CareerjetAPIClient("your_api_key")

    # Define job types and countries
    job_types = [
        "software engineer", "data scientist", "frontend developer",
        "backend developer", "full stack developer", "devops engineer",
        "mobile developer", "UI UX designer", "product manager",
        "data analyst", "machine learning engineer", "cloud engineer",
        "system administrator", "QA engineer", "security engineer",
        "blockchain developer", "AI engineer", "database administrator",
        "web developer", "IT support"
    ]

    countries = [
        "United States", "India", "United Kingdom", "Canada", "Australia",
        "Germany", "France", "Netherlands", "Singapore", "Japan",
        "Brazil", "Spain", "Italy", "Sweden", "Ireland",
        "Norway", "Denmark", "Belgium", "Switzerland", "New Zealand"
    ]

    # Create timestamp for unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"careerjet_all_jobs_{timestamp}.csv"

    # Write header to CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'job_type', 'country', 'title', 'company', 'locations',
            'salary', 'url', 'description', 'date', 'company_url',
            'salary_min', 'salary_max', 'salary_currency'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    # Use ThreadPoolExecutor for parallel execution
    tasks = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for job_type in job_types:
            for country in countries:
                tasks.append(executor.submit(fetch_jobs, cj, job_type, country))

        for future in as_completed(tasks):
            try:
                job_type, country, jobs = future.result()
                if jobs:
                    print(f"Writing {len(jobs)} jobs for {job_type} in {country}...")
                    job_data = [
                        {
                            'job_type': job_type,
                            'country': country,
                            'title': job.get('title', ''),
                            'company': job.get('company', ''),
                            'locations': job.get('locations', ''),
                            'salary': job.get('salary', ''),
                            'url': job.get('url', ''),
                            'description': job.get('description', ''),
                            'date': job.get('date', ''),
                            'company_url': job.get('company_url', ''),
                            'salary_min': job.get('salary_min', ''),
                            'salary_max': job.get('salary_max', ''),
                            'salary_currency': job.get('salary_currency', '')
                        }
                        for job in jobs
                    ]
                    save_jobs_to_csv(output_file, job_data)
            except Exception as e:
                print(f"Error processing job-country combination: {str(e)}")

if __name__ == "__main__":
    main()
