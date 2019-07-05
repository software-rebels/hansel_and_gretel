
set -e
echo "Installing dependencies!"
pip install -r requirements.txt
export MOOD="happy"
echo $MOOD
