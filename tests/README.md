## Unit Testing

In order to run the `unittest` tests included with this repository, you will need to set the 
`PYTHONPATH` environment variable to the `src` path of this repository and run `python -m unittest` 
from within the `tests` directory.

All provided examples assume that your working directory is the root of this repository.

**Powershell**
```powershell
# Set the PYTHONPATH env variable to the source directory.
Set-Location -Path "src"
$env:PYTHONPATH = $(Get-Location).Path

# Enter the tests directory and executes the unit tests.
Set-Location -Path "..\tests"
python -m unittest
```

**Bash**
```bash
# Set the PYTHONPATH env variable to the source directory.
cd "src"
export PYTHONPATH = $(pwd)

# Enter the tests directory and executes the unit tests.
cd "..\tests"
python -m unittest
```