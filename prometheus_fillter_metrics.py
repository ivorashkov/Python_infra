import time
import requests
from prometheus_client import start_http_server, Gauge, CollectorRegistry
from prometheus_client.exposition import basic_auth_handler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Create a custom registry
registry = CollectorRegistry()

# Define Prometheus metrics
url_up_metric = Gauge('sample_external_url_up', 'HTTP status up for the URL', ['url'], registry=registry)
response_time_metric = Gauge('sample_external_url_response_ms', 'Response time in ms for the URL', ['url'], registry=registry)

# List of URLs to check
urls = ['https://httpstat.us/503', 'https://httpstat.us/200']

# Function to check HTTP status and response time
def check_url_status():
    for url in urls:
        try:
            # Send GET request and measure the response time
            start_time = time.time()
            response = requests.get(url)
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds

            # Set up metric for response time
            response_time_metric.labels(url=url).set(response_time)

            # Set up metric for up/down status (1 if status code is 200, else 0)
            if response.status_code == 200:
                url_up_metric.labels(url=url).set(1)
            else:
                url_up_metric.labels(url=url).set(0)

        except requests.exceptions.RequestException:
            # In case of failure, consider the URL as down
            response_time_metric.labels(url=url).set(0)
            url_up_metric.labels(url=url).set(0)

# Function to run the HTTP server and start the periodic checks
def run_service():
    # Start the Prometheus HTTP server to expose the metrics
    start_http_server(8000, registry=registry)
    
    # Initialize scheduler to run check_url_status every 10 seconds
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        check_url_status,
        trigger=IntervalTrigger(seconds=10),
        id='url_check_job',
        name='Check URL status every 10 seconds',
        replace_existing=True
    )
    scheduler.start()

    # Keep the main thread alive to allow background tasks to run
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass

# Run the service
if __name__ == '__main__':
    run_service()
