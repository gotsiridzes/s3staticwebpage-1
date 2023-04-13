# AWS BTU
# S3 CLI + host static

That's S3 CLI tool, created for educational purposes. Don't forget to check `.env.example` file to see all the required credentials to allow CLI script work correctly.

## Install
First install:
```
https://github.com/ahupp/python-magic
```

```
poetry install
```

## Usage

First run in shell help command, to see the message about avaliable CLI functions, it can listen for passed `-h`, or `--help`:

## Host
Host website & enable public read 

```shell
python main.py host "your-bucket-name" --source "index.html"
```


Host static file with folders

```shell
python main.py host "your-bucket-name" --source "separate_project"
```
