
deactivate
echo "Deactivated"

rm -fdr venv
echo "VENV Deleted"

python3 -m venv venv
echo "New VENV Created"

. venv/bin/activate 
echo "New VENV Activated"

pip install --upgrade pip wheel
pip install --upgrade poetry
poetry install --no-cache