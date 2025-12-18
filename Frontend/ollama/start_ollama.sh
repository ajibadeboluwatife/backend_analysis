#!/bin/sh
ollama serve &
sleep 10
ollama pull gemma:2b
tail -f /dev/null