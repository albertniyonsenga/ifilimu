# 🎬 ifilimu

**ifilimu** is a simple yet powerful command-line tool to fetch and summarize movie information from a backend API.

![PyPI](https://img.shields.io/pypi/v/ifilimu)
![Python](https://img.shields.io/badge/python-3.12+-blue)
![License](https://img.shields.io/github/license/albertniyonsenga/ifilimu)

---

## Features

- Search for movie details from a remote backend
- Save results locally as JSON
- Display info in a beautiful Rich terminal layout
- Resilient with retry logic and graceful error handling

---

## 📦 Installation

```
pip install ifilimu
```
## Usage

```
ifilimu fetch --title "Oppenheimer"
```
To save the result as a local `.json` file:

```
ifilimu fetch --title "Inception" --save
```
## Environment Setup
If you're developing locally, creat a `.env` file with:
```
ENV=local
BACKEND_URL=http://localhost:10000
```
For production use:
```
ENV=production
BACKEND_URL=https://your-live-api.com
```
## Development
Clone this repo:
```
git clone https://github.com/albertniyonsenga/ifilimu
cd ifilimu
pip install -e .
```
And Run with:
```
ifilimu fetch --title "Your Movie"
```