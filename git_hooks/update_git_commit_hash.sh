#!/bin/bash

# Get the current git commit hash
commit_hash=$(git rev-parse HEAD)

# Set the git commit hash as an environment variable
export GIT_COMMIT_HASH=$commit_hash
