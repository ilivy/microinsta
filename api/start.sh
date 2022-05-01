#! /usr/bin/env bash

# Start API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 80