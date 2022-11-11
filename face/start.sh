#! /usr/bin/env bash

# Start API server
uvicorn main:app --reload --host 0.0.0.0 --port 8081