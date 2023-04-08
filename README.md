# Install Dependencies

In order to start worker for background request, you need to install redis on your system.

Install dependenies from requirement (virtualenv recomended).

```sh
$ pip install -r requirement.txt
```

# Run webservice
```sh
$ python manage.py runserver
```

# Run worker
In separate terminal run this command to start background worker
```sh
$ python manage.py rqworker default high low
```

Access the app from browser at http://127.0.0.1:8000
