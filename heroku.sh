#!/bin/bash
gunicorn app:app --daemon
python cron.py

