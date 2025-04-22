# Navigate to your project directory (change this if needed)
cd "C:\Users\Marjan\Documents\Python Code\python-data-playground"

# Remove the existing virtual environment if it exists
Remove-Item -Recurse -Force .venv

# Create a new virtual environment
python -m venv .venv

# Activate the new virtual environment
. .\.venv\Scripts\Activate.ps1

# Upgrade pip (optional but recommended)
python -m pip install --upgrade pip

# Install required packages from your requirements.txt
pip install -r requirements.txt
