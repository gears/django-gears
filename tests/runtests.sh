#!/bin/bash

export PYTHONPATH=$PWD:$PWD/..:$PYTHONPATH

django-admin.py test --settings=tests.settings_templatetags
django-admin.py test --settings=tests.settings_serve
