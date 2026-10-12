# SCCD-X Engine — container image.
#
# Works as a plain Docker run and as a Hugging Face Space (SDK: docker),
# which expects the app on port 7860. serve.py already reads SCCDX_HOST and
# SCCDX_PORT from the environment, so no application change is needed.
#
#   docker build -t sccdx-engine .
#   docker run --rm -p 7860:7860 sccdx-engine
#   → http://127.0.0.1:7860
FROM python:3.12-slim

# scipy is optional for the engine but it is the stiff solver the source
# paper actually mandates, so the image ships with it.
RUN pip install --no-cache-dir numpy scipy

# Hugging Face Spaces run as uid 1000 and the image must not need root.
RUN useradd -m -u 1000 app
WORKDIR /home/app
COPY --chown=app:app . /home/app
USER app

ENV SCCDX_HOST=0.0.0.0 \
    SCCDX_PORT=7860 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

EXPOSE 7860

# Fail the build rather than ship a broken image.
RUN python validate2.py > /dev/null

CMD ["python", "serve.py"]
