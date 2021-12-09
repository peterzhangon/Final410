# ExpertSearch

# Part-1: Overview of the develop ment ENV

* Basically, we install Ubunto 18.04 on windows 10 box.
* 1: We write code using Python IDE on windows box;
* 2: We run the web service on Ubunto;
* 3: We using Google chrome on Windows to query and display;

# Part-2: To install ubuntu on desktop directly

* Go to micrsoft store, and search ubuntu 18.04, and install it
* https://www.youtube.com/watch?v=X-DHaQLrBi8
* You may set up Ubunto username and password.

# Part-3: To install packages on Ubunto

- sudo apt-get update
- sudo apt install python
- sudo apt install python-pip
- sudo apt install gunicorn
- pip install flask
- pip install metapy
- pip install requests

# Part-4: To clone the code via git bash on windows or via terminal on Ubunto

We may put codes in fixed location, so we can access the code via Ubuntu and Windows

## The directory on Ubunto
- cd /mnt/c/code

## The folder on windows
- cd c:\code

# Part-5: pip list results

If you cannot start web service and query via web page, you may check the required packages have been installed or not.

- pip list
- asn1crypto (0.24.0)
- certifi (2021.10.8)
- chardet (4.0.0)
- click (7.1.2)
- cryptography (2.1.4)
- enum34 (1.1.6)
- Flask (1.1.4)
- Flask-Cors (3.0.10)
- gunicorn (19.7.1)
- idna (2.10)
- ipaddress (1.0.17)
- itsdangerous (1.1.0)
- Jinja2 (2.11.3)
- keyring (10.6.0)
- keyrings.alt (3.0)
- MarkupSafe (1.1.1)
- metapy (0.2.13)
- pip (9.0.1)
- pycrypto (2.6.1)
- pygobject (3.26.1)
- pytoml (0.1.21)
- pyxdg (0.25)
- requests (2.26.0)
- SecretStorage (2.3.1)
- setuptools (39.0.1)
- six (1.16.0)
- urllib3 (1.26.7)
- Werkzeug (1.0.1)
- wheel (0.30.0)
 
# Part-6: Source code location:

- https://github.com/peterzhangon/Final410


# Part-7: To clone the code:

- https://github.com/peterzhangon/Final410


# Part-8: To start web service
- gunicorn server:app -b 127.0.0.1:8095


# Part-9: To open the web page

- The site should be available at http://localhost:8095/