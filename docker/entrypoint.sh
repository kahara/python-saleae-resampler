#!/bin/bash -l
set -e
if [ "$#" -eq 0 ]; then
  exec saleae_resampler -vv docker_config.toml
else
  exec "$@"
fi
