coverage run manage.py test --parallel=6
printf "\n"
coverage combine
coverage report
coverage html
printf "\n"
flake8