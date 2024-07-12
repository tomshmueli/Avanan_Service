# Event Keyword Counter Service

## Background and Assumptions

This project implements a simple Python service that receives ongoing events of sentences and counts the occurrence of specific keywords: "checkpoint", "avanan", "email", and "security".

### Assumptions:

1. **Time Interval Handling**:
   - The `/stats` endpoint uses `start` and `end` parameters to define the time interval in seconds instead of 1 integer value "interval"
   - If `start` is not provided, it defaults to `0`.
   - If `end` is not provided, it defaults to the current time.

2. **Memory Usage**:
   - The service uses in-memory storage with the Data Structure called stats_time.
   - stats_time is a dictionary that stores the count of keywords for each second. 
   - stats[time_stamp] = {"checkpoint": 0, "avanan": 0, "email": 0, "security": 0}

3. **Sentence Assumptions**:
   - Keywords are case-insensitive and counted only when they appear as whole words.
   - Substrings within other words are not counted (e.g., "emailed" does not count as "email").

## Installations and Setup

1. **Clone the repository**:
   ```sh
   git clone <repository-url>
   cd <repository-directory>

2. **Install Docker**

3. **Build the Docker Image**:
   ```sh
   docker build -t event-service .

4. **Run the Docker Container**:
   ```sh
   docker run -d -p 8000:8000 event-service

5. **Access the Service**:
   - The service is now running on `http://localhost:8000`.

6. **Run the Tests**:
   - can be done from the tests folder directly or:
   ```sh
   python -m unittest discover -s tests

## Project Structure:
- **app/main.py:** Entry point for the FastAPI application. Initializes and configures the services.
- **app/api/events.py:** Defines the /events endpoint for receiving and processing sentences.
- **app/api/stats.py:** Defines the /stats endpoint for retrieving keyword counts within a specified time interval.
- **app/models/event.py:** Contains the Event model with the sentence and the global KEYWORDS.
- **app/models/event_service.py:** Implements the logic for processing events and maintaining keyword counts.
- **app/models/stats_service.py:** Implements the logic for querying statistics over specified intervals.
- **tests/test_main.py:** Unit tests for verifying the functionality of the endpoints and services.

## Scalability:
- **Async Processing:** The service uses asyncio for handling requests asynchronously, enabling it to scale with higher loads.
- **Efficient Interval Querying:** Custom binary search implementation ensures efficient querying of keyword counts within specified time intervals.
- **Dockerization:** The service can be containerized and deployed using Docker, making it easy to scale horizontally across multiple instances.
- **Project Structure:** The project is organized into separate modules for handling events, statistics, and API endpoints, making it easier to scale and maintain.
