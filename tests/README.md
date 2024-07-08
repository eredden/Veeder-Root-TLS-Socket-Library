## Unit Testing

The following script can used to execute unit tests against a development wheel of this package.

**Powershell:**

```powershell
# Remove previously built wheel of this package.
pip uninstall veeder_root_tls_socket_library --no-input

if (Test-Path -Path "build") {
    Remove-Item -Path "build" -Recurse -Force
}

if (Test-Path -Path "dist") {
    Remove-Item -Path "dist" -Recurse -Force
}

# Build a new wheel for this package and install it.
python -m build --wheel

Set-Location -Path "dist"
$wheel = $(Get-Location).Path + "\" + $(Get-ChildItem)[0].Name
Set-Location -Path ".."

python -m pip install $wheel

# Set environment variables before testing.
$env:TLS_IP   = "INSERT IP HERE"
$env:TLS_PORT = "INSERT PORT HERE"

# Run the tests.
Set-Location -Path "tests"

python -m unittest
```