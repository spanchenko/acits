## Solution for acits task

Run solution
1. Clone this repo and install some dependencies

```
git clone https://github.com/spanchenko/acits.git
cd acits
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd src/acits_task
```

2. Run some tests:

```
python manage.py test
```

3. Run dev server:

```
python manage.py runserver
```

4. Swagger UI available at http://localhost:8000/api/v1/schema/swagger-ui/

### P.S.
Not all filters \ search fields implemented as required in task due to low time limit

Not all nessecary tests are implemented