Find mentions of surveillance technology in law enforcement reports.

## Installation

1. Install Python 3.11+
2. [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) this project from GitHub
3. (Recommended) Create a [Python virtual environment](https://docs.python.org/3/library/venv.html) and activate it.
4. Run `pip install -r requirements.txt`
5. Run `python -m spacy download en_core_web_sm`
6. Move all of the pdfs into `data/tpsb`
7. Add a `names.txt` file (you can keep it empty) in `data/`
8. Run `python main.py`