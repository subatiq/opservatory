![](docs/brands/full_logo_white.svg#gh-dark-mode-only)
![](docs/brands/full_logo_black.svg#gh-light-mode-only)

<p align="center">
  <img alt="Code style" src="https://img.shields.io/badge/license-mozilla%20PL%202-black?style=for-the-badge">
  <img alt="Gitlab code coverage" src="https://img.shields.io/gitlab/coverage/subatiq/opservatory/master?style=for-the-badge">
  <img alt="Code style" src="https://img.shields.io/badge/code%20style-black-black?style=for-the-badge">
</p>

API for checking docker containers states in a small infrastructure

CLI https://github.com/subatiq/ops

---

## Quick start

Step 1.0  Put Kornet fleet.yml file into inventory

`opservatory/infrastructure/inventory/` <- file named fleet.yml should be here

NOTE: if you are using docker, put `fleet.yml` into `volumes/inventory`

Step 1.5  Replace company name in config.json

Step 2.0  Run locally

```
uvicorn opservatory.api:app --host 0.0.0.0 --port 5000
```

or 

```
docker build -t opservatory .
docker run -p 5000:5000 opservatory
```

## To add/remove device

1. Stop running container
2. Remove `volumes/state.json`
3. Edit `volumes/inventory/fleet.yml`
4. Start container again

---

Made by [Subatiq](https://github.com/subatiq) for the team of INVIAN. Powered by [Kornet](https://subatiq.github.io/kornet/)
