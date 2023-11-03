#/bin/bash
# This file is to be called from build_conda.sh
# and not run directly.

# pip install --upgrade pip
pip install wheel setuptools
# Get the machine hardware type
machine_arch=$(uname -m)

# Check if it's an Apple Silicon Mac
if [ "$machine_arch" = "arm64" ]; then
  echo "This is an Apple Silicon Mac.  Installing compiler directives"
  export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1
  export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1
else
  echo "This is not an Apple Silicon Mac."
fi

git pull
python -m pip install -e .
