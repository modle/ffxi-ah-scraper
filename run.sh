export SCRIPT_PATH="/home/matt/workspace/ah-scraper"
source $SCRIPT_PATH/venv/bin/activate
python $SCRIPT_PATH/run.py
cat "$SCRIPT_PATH/run.sh" | at now + 5 minutes
