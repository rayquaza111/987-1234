# OptiSigns – OptiBot Mini-Clone Take-Home Test

## Setup
* Python 3.11+
* Make a copy of `.env.sample` and rename it to `.env`.
* Add your Gemini `API_KEY` into the `.env` file.

## How to Run Locally

Clone this repo: 
   `git clone https://github.com/rayquaza111/987-1234.git`

**Option 1: Run with Python**
```bash
python -m venv .venv
source .venv/bin/activate  # (or .venv\Scripts\activate on Windows)
pip install -r requirements.txt
python main.py
```

**Option 2: Run with Docker**
To test the container strictly with a passed environment variable (runs once and exits 0):
```bash
docker build -t sync-bot .
docker run -e API_KEY="your_api_key" sync-bot
```

## Link to Daily Job Logs
The scraper is scheduled as a daily job on Render at 06:00 AM. 
<img width="2540" height="1249" alt="image" src="https://github.com/user-attachments/assets/841572d9-a8b5-410f-9b77-2806faaa9a0d" />

Because the live cloud console is private, here is my last run artefact:
[https://github.com/rayquaza111/987-1234/blob/main/last_run_logs.txt](https://github.com/rayquaza111/987-1234/blob/main/last_run_logs.txt)

## Screenshot of Assistant Answering a Sample Question
<img width="1031" height="610" alt="image" src="https://github.com/user-attachments/assets/655ed97a-fa88-4f50-a7e4-c9152e71afd8" />
