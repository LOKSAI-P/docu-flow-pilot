
#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install requirements
pip install -r requirements.txt

# Run the FastAPI server in development mode
cd api
uvicorn api:app --host 0.0.0.0 --port 8000 --reload

echo "Server is running at http://localhost:8000"
