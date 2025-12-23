FROM ollama/ollama

COPY start_ollama.sh /start_ollama.sh

RUN chmod +x /start_ollama.sh

EXPOSE 11434

ENTRYPOINT [ "./start_ollama.sh" ]