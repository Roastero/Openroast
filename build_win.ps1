# process command-line arguments
param (
    [string]$branch_name = "master", # name of branch to work with
    [switch]$tool_install = $false, # install necessary tools to build release
    [switch]$git_fetch = $false, # fetch project using git
    [switch]$python_build_tool_install = $false, # install necessary python packages to build release
    [switch]$bump_ver_maj = $false, # increment major version number
    [switch]$bump_ver_min = $false, # increment minor version number
    [switch]$bump_ver_patch = $false,   # increment patch number
    [switch]$bump_ver_release = $false, # move from dev->alpha->beta->rc->release
    [switch]$bump_ver_iter = $false,  # increment iteration for dev/a/b/rc by default
    [switch]$make_installer = $false # create the installer
)
# remember current directory
$crnt_folder = $PSScriptRoot
# installing fundamental tooling to build project
if( $tool_install )
{
    Write-Output( "Installing tools...")
    # go to a standard place - home directory a good idea...
    cd ~
    # get the location of a temporary dir where we can download stuff
    $tempDir = [io.path]::GetTempPath()
    # prepare WebClient for use
    $wclient = New-Object System.Net.WebClient
    # download python 3.5 - 64-bit
    $pythonInstallerFileName = "python-3.5.3-amd64.exe"
    $pythonUrl = "https://www.python.org/ftp/python/3.5.3/" + $pythonInstallerFileName
    $pythonInstallerDestFileName = $tempDir + $pythonInstallerFileName
    $destFileExists = Test-Path $pythonInstallerDestFileName
    if( $destFileExists -eq $true ) {
        Write-Output "Python installer already downloaded - use it!"
    }
    else {
        Write-Output "Downloading python installer " $dlUrl
        Write-Output "Saving to " $pythonInstallerDestFileName
        $wclient.DownloadFile($pythonUrl,$pythonInstallerDestFileName) 
    }
    # download Git for Windows 2.11.1 64 bit
    $gitInstallerFileName = "Git-2.11.1-64-bit.exe"
    $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.11.1.windows.1/" + $gitInstallerFileName
    $gitDestFileName = $tempDir + $gitInstallerFileName
    $destFileExists = Test-Path $gitDestFileName
    if( $destFileExists -eq $true ) {
        Write-Output "Git installer already downloaded - use it!"
    }
    else {
        Write-Output "Downloading git for windows installer " $gitUrl
        Write-Output "Saving to " $gitDestFileName
        $wclient.DownloadFile($gitUrl,$gitDestFileName) 
    }
    # Download NSIS 3.01
    $nsisInstallerFileName = "nsis-3.01-setup.exe"
    $nsisUrl = "https://sourceforge.net/projects/nsis/files/NSIS%203/3.01/" + $nsisInstallerFileName
    $nsisDestFileName = $tempDir + $nsisInstallerFileName
    $destFileExists = Test-Path $nsisDestFileName
    if( $destFileExists -eq $true ) {
        Write-Output "NSIS installer already downloaded - use it!"
    }
    else {
        Write-Output "Downloading NSIS for windows installer " $nsisUrl
        Write-Output "Saving to " $nsisDestFileName
        $wclient.DownloadFile($nsisUrl,$nsisDestFileName) 
    }
    # install python
    Write-Output "Installing " $pythonInstallerFileName
    $args = "/passive PrependPath=1"
    $check = Start-Process $pythonInstallerDestFileName -ArgumentList $args -Wait -Verb RunAs
    # install git
    Write-Output "Installing " $gitInstallerFileName
    $args = "/SILENT"
    $check = Start-Process $gitDestFileName -ArgumentList $args -Wait -Verb RunAs
    # install NSIS
    Write-Output "Installing " $nsisInstallerFileName
    $args = "/S"
    $check = Start-Process $nsisDestFileName -ArgumentList $args -Wait -Verb RunAs
    # return to original directory
    cd $crnt_folder
}
# pulling the project using git
if( $git_fetch )
{
    Write-Output( "Fetching project using git...")
    # this script can be pulled from github separately and run from anywhere.
    # let's determine if we're in the project dir or not
    if( (Test-Path ".\openroast") -eq $false )
    {
        # we assume we are just outside the project root, where the user wants 
        # the project created
        # we'll CD into that folder once we're done.
        if( (Test-Path ".\Roastero\Openroast") -eq $false )
        {
            # project isn't there, so clone it
            New-Item -ItemType Directory -Force -Path ".\Roastero"
            cd Roastero
            Write-Output "cloning project..."
            git clone https://github.com/Roastero/Openroast.git
            cd Openroast
        }

    }
    # we should now be in the project root
    # project is there, need to reset to master HEAD?
    Write-Output "openroast git project already on disk. Set local to match remote master?"
    $answer = Read-Host "yes or no"
    while( "yes","no" -notcontains $answer)
    {
        $answer = Read-Host "yes or no"
    }
    if("yes" -contains $answer)
    {
        git fetch origin
        git reset --hard origin/$branch_name
    }
}
# beyond this point, if we do not have access to openroast code,
# there's nothing more we can really do.
if( (Test-Path ".\openroast") -eq $false )
{
    Write-Error "No project files to build with. Please invoke this script with -git_fetch at least once to fetch files!"
    return
}
# there are more tools to install within python for building, as specified in
# the openroast project.
if( $python_build_tool_install )
{
    Write-Output( "Installing python build tools listed in build-app-requirements.txt & build-win-tool-requirements.txt...")
    # install python packages required to be specifically installed as pkg 
    # to be imported by pynsist
    pip install -U -r build-app-requirements.txt
    # install python packages required to create the build
    pip install -U -r build-win-tool-requirements.txt
}
# increment version as requested
if( $bump_ver_maj )
{
    Write-Output( "Incrementing major build number...")
    bumpversion major
}
elseif( $bump_ver_min )
{
    Write-Output( "Incrementing minor build number...")
    bumpversion minor
}
elseif( $bump_ver_patch )
{
    Write-Output( "Incrementing patch build number...")
    bumpversion patch
}
elseif( $bump_ver_release )
{
    Write-Output( "Incrementing release (dev->a->b->rc->'')...")
    bumpversion release
}
elseif( $bump_ver_iter )
{
    Write-Output( "Incrementing iteration number...")
    bumpversion iter
}
# make the windows installer
if( $make_installer )
{
    Write-Output( "making Windows installer...")
    if( (Test-Path "pynsist_installer.cfg") -eq $false )
    {
        Write-Error("pynsist_installer.cfg not found.  Have you run this script with tool_install, git_fetch, and python_build_tool_install first?")
        return
    }
    # deleting any existing build stuff
    # Need to call this twize for it to really work... because, Microsoft...
    Remove-Item -Recurse -Force build
    Remove-Item -Recurse -Force build
    # read in version number
    $version = ((((Get-Content 'openroast\version.py') -split "\s",3)[2]) -split "`"",3)[1]
    Write-Output( "Using version number " + $version )
    $pynsist_filename = "pynsist_installer_" + $version + ".cfg"
    # create a temp file with the current version number
    If (Test-Path $pynsist_filename)
    {
        Remove-Item $pynsist_filename
    }
    # find and replace %VERSION% string with $version
    (Get-Content pynsist_installer.cfg).replace('%VERSION%', $version) | Set-Content $pynsist_filename
    pynsist $pynsist_filename
    Remove-Item $pynsist_filename
}
