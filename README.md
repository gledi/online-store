SDA Albania - Python Tirana 6
=============================

Backend Programming Sample App
------------------------------

Clone the code:

```
git clone https://github.com/gledi/online-store.git
```

Enter the directory where the code was cloned and create a virtual environment

```
cd online-store
python -m venv venv
```

Activate the virtual environment

```
# if you are using command prompt
venv\Scripts\activate
# If you are using powershell
. venv\Scripts\activate
# If you are on MacOS or Linux
. venv/bin/activate
```

Install the required packages

```
pip install -r requirements.txt
```

Apply migrations
```
python manage.py migrate
```

Run the development server
```
python manage.py runserver
```
