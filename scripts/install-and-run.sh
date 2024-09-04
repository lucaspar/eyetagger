#!/usr/bin/env bash

set -euo pipefail

APP_PORT=${APP_PORT:-8000}
DEBUG=${DEBUG:-False}

function say_err() {
    echo -e "\e[34m[$(date +'%Y-%m-%dT%H:%M:%S%z')]\e[31m $*\e[0m"
}

function say() {
    echo -e "\e[34m[$(date +'%Y-%m-%dT%H:%M:%S%z')]\e[36m $*\e[0m"
}

function system-setup() {
    # add global yarn tools to container / runtime env.
    yarn add global @vue/cli
    yarn global add npx
}

function install-project() {
    uv sync
    yarn install --production=false
}

function run-project() {
    uv run ./manage.py collectstatic --no-input
    uv run ./manage.py makemigrations
    uv run ./manage.py migrate
    if [ "$DEBUG" == "True" ]; then
        yarn serve &
        uv run ./manage.py runserver
    else # assume production environment
        yarn build --no-clean
        uv run gunicorn --log-level debug --access-logfile - \
            --workers 3 --bind "0.0.0.0:$APP_PORT" backend.wsgi:application
    fi
}

function upgrade-project() {
    uv sync --upgrade
    yarn upgrade
}

function precondition-checks() {
    if [ ! -f "package.json" ]; then
        say_err "package.json not found. Are you in the right directory?"
        exit 1
    fi
    if [ ! -f "manage.py" ]; then
        say_err "manage.py not found. Are you in the right directory?"
        exit 1
    fi
    if [ ! -f "pyproject.toml" ]; then
        say_err "pyproject.toml not found. Are you in the right directory?"
        exit 1
    fi
    if ! command -v uv &>/dev/null; then
        say_err "uv is not installed. Please install it."
        exit 2
    fi
    if ! command -v yarn &>/dev/null; then
        say_err "yarn is not installed. Please install it."
        exit 2
    fi
}

function main() {
    say "Starting install-and-run script"
    say "Environment: DEBUG=$DEBUG, APP_PORT=$APP_PORT"
    precondition-checks
    system-setup
    say "Running installing project"
    install-project
    upgrade-project
    say "Running project"
    run-project
}

main