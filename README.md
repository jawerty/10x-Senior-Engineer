# 10x-Senior-Engineer
An [Code Llama](https://about.fb.com/news/2023/08/code-llama-ai-for-coding/) agent that watches your repo for file changes and asks code llama to review your code and responds with code reviews and "LGTM" files that pass.

Example usage
```
$ python senior-engineer.py --api=http://382e-34-143-193-144.ngrok.io /path/to/your/repo/folder
```

I built 10x-Senior-Engineer on this [this live stream](https://www.youtube.com/watch?v=C9ALpMH3trI) on my Youtube. It works pretty good.

# How it works
10x-Senior-Engineer runs on it's own process and waits for file changes. As it gets new file changes it will generate code reviews using the API you set up in Colab. It will keep a queue of the past 10 files that have been reviewed.

10x-Senior-Engineer currently using a flask api running from a [Google Colab](https://colab.research.google.com/drive/18_qsyN1fZEZ0o0Qju-SLF_pqQv53Mk8_?usp=sharing) to prompt Code Llama. If you want to change this to use llama.cpp please create an issue and I'll try to address it.

# How to use it
### Set up the Google Colab 
Go to the [Google Colab](https://colab.research.google.com/drive/18_qsyN1fZEZ0o0Qju-SLF_pqQv53Mk8_?usp=sharing) and run the server and copy the ngrok url

You have to run all the cells and ensure the flask server is running properly

Example ngrok url below


### Clone the repo
```

$ git clone git@github.com:jawerty/10x-Senior-Engineer
$ cd 10x-Senior-Engineer
```

### Install the packages
```
$ pip install -r requirements.txt
```

The arguments/options
```
usage: senior-engineer.py [-h] [--api API] repository

positional arguments:
  repository  Pass in the source code folder you want to watch

options:
  -h, --help  show this help message and exit
  --api API   Link to the colab ngrok url
```

### Run it
Example command
```
$ python senior-engineer.py --api=http://382e-34-143-193-144.ngrok.io /path/to/your/repo/folder

```

# Have fun!
