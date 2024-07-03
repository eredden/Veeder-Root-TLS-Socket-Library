## Unit Testing

In order to run the `unittest` tests included with this repository, 
you will need to do the following:
1. Set the `PYTHONPATH` environment variable to the `src` path of this repository.
2. Set the `TLS_IP` and `TLS_PORT` environment variables to point to your Veeder-Root system.
3.  Run `python -m unittest` from within the `tests` directory.

These steps can be accomplished using the below scripts.
All provided examples assume that your working directory is the root of this repository.

**Powershell**
```powershell
# Set the TLS_IP and TLS_PORT env variables to point to your Veeder-Root automatic tank gauge.
$env:TLS_IP   = "REPLACE WITH IP ADDRESS OF YOUR TLS SYSTEM"
$env:TLS_PORT = "REPLACE WITH PORT OF YOUR TLS SYSTEM"

# Set the PYTHONPATH env variable to the source directory.
Set-Location -Path "src"
$env:PYTHONPATH = $(Get-Location).Path

# Enter the tests directory and executes the unit tests.
Set-Location -Path "..\tests"
python -m unittest
```

**Bash**
```bash
# Set the TLS_IP and TLS_PORT env variables to point to your Veeder-Root automatic tank gauge.
export TLS_IP   = "REPLACE WITH IP ADDRESS OF YOUR TLS SYSTEM"
export TLS_PORT = "REPLACE WITH PORT OF YOUR TLS SYSTEM"

# Set the PYTHONPATH env variable to the source directory.
cd "src"
export PYTHONPATH = $(pwd)

# Enter the tests directory and executes the unit tests.
cd "..\tests"
python -m unittest
```