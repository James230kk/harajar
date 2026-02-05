#!/bin/sh
# Expand PORT so Railway (and others) pass a real port number to gunicorn
PORT="${PORT:-5000}"
exec gunicorn dashboard:app --bind "0.0.0.0:${PORT}" --workers 2 --timeout 120
