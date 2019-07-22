# Evaluation Backend

![](https://flat.badgen.net/circleci/github/SecureCats/Evaluation_BackEnd?icon=circleci)
![](Evaluation_FrontEnd/coverage/badge-branches.svg)
![](Evaluation_FrontEnd/coverage/badge-lines.svg)
![](Evaluation_FrontEnd/coverage/badge-statements.svg)

> Backend server for TAPES | The totally anonymous professor evaluation system.

## Building

1. Install dependencies

```shell
pipenv install
```

2. Enter virtual environment

```shell
pipenv shell
```

3. Migrate Django database

```shell
python manage.py migrate
```

4. Run python server

```shell
python manage.py runserver
```

## API

### Initialization

`/api/v1/init?classno={class_no}&semester={semester}`

### Authentication

`/api/v1/auth?course_no={course_no}&class_no={classno}`