#!/bin/bash

set -e

export PYTHONPATH=$PWD:$PWD/..:$PYTHONPATH

django-admin.py test --settings=tests.settings_get_asset_handler
django-admin.py test --settings=tests.settings_get_finder
django-admin.py test --settings=tests.settings_templatetags
django-admin.py test --settings=tests.settings_serve
