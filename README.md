How fast can one push notifications to SNS?
===========================================
Prerequisites:
```
$ sudo apt-get install python-setuptools
$ sudo apt-get install python-pip
$ sudo pip install virtualenv
```

Application:
```
$ git clone https://github.com/eliwjones/sns_throughput_test.git
$ cd sns_throughput_test
$ virtualenv venv --distribute
$ source venv/bin/activate
$ pip install boto gevent
```

Make sure to add your EC2 information to config.py!
