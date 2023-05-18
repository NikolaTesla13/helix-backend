# Helix backend

The backend for the Helix website. You can find the frontend [here](https://github.com/NikolaTesla13/helix).

# Required software

You need to have installed the following software:

- Python 3
- Docker
- G++ >= 11

# How to run

Clone the repository:

```bash
git clone https://github.com/NikolaTesla13/helix-backend.git
```

Go to the directory:

```bash
cd helix-backend
```

## For development

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file with the following values:

```python
DEV=True
# your HuggingFace free API key
HF_API_KEY=
```

Start the local web server:

```bash
python3 run.py
```

Now the server should run on localhost:4000.

## For deployment

Build the docker image:

```bash
docker build -t helix-backend .
```

Start the container:

```bash
docker run -dp 4000:4000 helix-backend
```
