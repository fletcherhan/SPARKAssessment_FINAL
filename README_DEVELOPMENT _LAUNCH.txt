To launch the website locally:
(1) Run the following into the terminal: >>. venv/bin/activate 
(2) Run the following on if on a new computer, if not new computer, skip to the third step:
    (2a) run: >> pip install flask
    (2b) run: >> FLASK_ENV = development
(3) enter: >> export FLASK_ENV=development
(4) enter: >> flask run

Coming to Mac from Windows changes:
(1) Delete "venv" folder
(2) run: >> python3 -m venv venv
(3) run: >>. venv/bin/activate
(3) run: >> export FLASK_ENV=development
(4) run: >> flask run

To push all files to GitHub Repo:
(1) Go to GitHub and create a repository
(2) Pull that repository locally in your terminal by running: >> git clone ________ <-- URL provided
(3) Drag your files in to the GitHub repo that is now locally on your computer
(4) Push changes by running: >> git status, then >> git add ., then >>git commit -m “comment changes made”, then >> git push origin main (or master)

Before uploading:
(1) Delete venv file

Running on window:
(1) if venv does not exist, run: >> py -3 -m venv venv
(2) run: >> venv\Scripts\activate
(3) run: >> $env:FLASK_ENV="development"
(4) run: >> flask run
 
 