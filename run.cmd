@Echo off
call secrets.cmd
@Echo on

set FLASK_APP=cs50w_project1.py
set DATABASE_URL=postgres://%DB_USERNAME%:%DB_PASSWORD%@%DB_HOST%:%DB_PORT%/%DB_NAME%
set FLASK_DEBUG=1

flask run