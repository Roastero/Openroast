#!/bin/sh

# COMMAND LINE ARGS PARSING
# Use -gt 1 to consume two arguments per pass in the loop (e.g. each
# argument has a corresponding value to go with it).
# Use -gt 0 to consume one or more arguments per pass in the loop (e.g.
# some arguments don't have a corresponding value to go with it such
# as in the --default example).
# note: if this is set to -gt 0 the /etc/hosts part is not recognized ( may be a bug )
# deftauls
branch_name="master"
git_fetch=false
show_help=false
python_build_tools_install=false
no_warn_profile=false
bump_version=false
bump_part="none"
make_install=false
# parse cmd line
while [ $# -gt 0 ]
do
    key="$1"
    # echo KEY = "$key"
    case $key in
        '-n' | '--no_warn_profile')
            no_warn_profile=true
        ;;
        '-b' | '--branch')
            branch_name="$2"
            shift # past argument
        ;;
        '-f' | '--fetch')
            git_fetch=true
        ;;
        '-p' | '--python_reqs')
            python_build_tools_install=true
        ;;
        '-m' | '--make_install')
            make_install=true
        ;;
        '-i' | '--increment_version')
            bump_version=true
            bump_part="$2"
            shift # past argument
        ;;
        '-h' | '--help' )
            show_help=true
        ;;
        *)
                # unknown option
        ;;
    esac
    shift # past argument or value
done
# if SHOW_HELP, show help, then exit
if [ "${show_help}" = true ] ; then
    echo "usage: build_mac.sh [-b|--branch <branch_name>][-h|--help][-f|fetch]

Build and package Openroast for OS X.

Arguments:
    -n --no_warn_profile
        Acknowledge one-time profile setting warnings.
        Script will not run to completion without this argument.
    -f --fetch
        get HEAD from git repo from branch specified with --branch option.
    -b --branch <branch_name>
        name of branch to use to fetch source.  
        Defaults to master if not specified.
    -p --python_reqs
        Install python app requirements and python build tools for
        the Mac version of this app, as specified in 
        build-mac-tool-requirements.txt.
    -m --make_install
        build the Openroast application.
    -i --increment_version <part>
        increment the specified part of the version number.
        X.Y.ZRI (e.g. 1.2.0a4)
        to increment:  specify <part>:
        X              major
        Y              minor
        Z              patch
        R              release ('dev'->'a'->'b'->'rc'->'')
    -h --help
        view this usage statement."
    exit
fi
# otherwise, run the script with the desired arguments
echo
echo Arguments:
echo ----------
echo no_warn_profile = "${no_warn_profile}"
echo branch_name  = "${branch_name}"
echo git_fetch = "${git_fetch}"
echo make_install = "${make_install}"
echo python_build_tools_install = "${python_build_tools_install}"
echo

# TOOLS INSTALL
echo 'Checking build tools...'
which -s brew
if [[ $? != 0 ]] ; then
    # Install Homebrew
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
# else
    # brew update
fi

# PYTHON INSTALL
echo 'Checking for python 3.5.3...'
# We use python 3.5 because PyQt5 is easier to deal with in 3.5+
# Use pyenv to install a specific python version
which -s pyenv
if [[ $? != 0 ]] ; then
    # Install pyenv
    brew install pyenv 
fi
# check if 3.5.3 already installed, install & switch as necessary
installed_py_versions=$(pyenv versions)
# echo "${installed_py_versions}"
if [[ "${installed_py_versions}" != *"3.5.3"* ]]; then
    echo "Installing python 3.5.3 with enable-framework option..."
    env PYTHON_CONFIGURE_OPTS="--enable-framework" pyenv install 3.5.3  
fi
echo "Switching to python 3.5.3..."
pyenv local 3.5.3
pyenv versions
# for this to work, you'll need some stuff in your .bash_profile
if [ ! -f ~/.bash_profile ]; then
    echo "export PYENV_ROOT=\"$HOME/.pyenv\"
export PATH=\"$PYENV_ROOT/bin:$PATH\"
eval \"$(pyenv init -)\"" >> ~/.bash_profile
    echo "Created ~/.bash_profile.  Please close and re-start
Terminal for the changes to take effect."
    exit
else
    if ! "${no_warn_profile}" ; then
        echo "YOU MUST HAVE a ~/.bash_profile file with
the following lines in it for pyenv to work:

export PYENV_ROOT=\"\$HOME/.pyenv\"
export PATH=\"\$PYENV_ROOT/bin:\$PATH\"
eval \"\$(pyenv init -)\"

Please ensure this is the case.  Then, use the -n option
with this script to avoid this warning. -h for help. Abort."
        exit
    fi
fi

# GIT PROJECT FETCH
# Decide if this script is already in the project directory
# If so, just assume we can use this folder as the project root
# Else, create project root and cloen project into it
if [ "${git_fetch}" = true ] ; then
    echo "Fetching project using git..."
    # this script can be pulled from github separately and run from anywhere.
    # let's determine if we're in the project dir or not
    if [ ! -d "./openroast" ]; then
        echo "This script is not in the project folder - creating project folder..."
        if [ ! -d "./Roastero/Openroast" ]; then
            echo "Creating /Roastero/Openroast folder..."
            if [ ! -d "./Roastero" ]; then
                mkdir Roastero
            fi
            cd Roastero
            git clone https://github.com/Roastero/Openroast.git
            cd Openroast
            # we should now be in the project root
        fi
    fi
    # project is there, need to reset to master HEAD?
    while true; do
        read -p "openroast git project on disk. Fetch remote now?" yn
        case $yn in
            [Yy]* )
                git checkout "${branch_name}";
                git fetch origin; 
                git reset --hard origin/"${branch_name}"; 
                break;;
            [Nn]* ) 
                break;;
            * ) echo "Please answer yes or no.";;
        esac
    done    
fi

# beyond this point, if we do not have access to openroast code,
# there's nothing more we can really do.
if [ ! -d "./openroast" ]; then
    echo "No project files to build with. Please check errors."
    exit
fi

# PYTHON BUILD TOOLS INSTALL
# there are more tools to install within python for building, as specified in
# the openroast project.
if [ "${python_build_tools_install}" = true ] ; then
    echo "Installing python build tools listed in build-mac-tool-requirements.txt..."
    # install python packages required to create the build
    pip install -U -r build-app-requirements.txt
    pip install -U -r build-mac-tool-requirements.txt
fi    

# INCREMENT VERSION NUMBER
if "${bump_version}" ; then
    bumpversion "${bump_part}"
fi

# BUILD THE APP
if "${make_install}" ; then
    echo "make_install - creating Openroast app..."
    # remove old stuff
    rm -rf build dist
    # get version string
    version_file=($(<openroast/version.py)) 
    version_string=$(echo ${version_file[2]} | tr -d '"')
    echo "Using version_string = ${version_string}"
    version_mmp=$(echo ${version_string} | sed -E 's/[A-Za-z]+[0-9]+//')
    echo "Using version_mmp = ${version_mmp}"
    sed -E -e 's/%VERSION%/'"${version_string}"'/' -e 's/%VERSION_MMP%/'"${version_mmp}"'/' <setup_py2app.py >setup_py2app_"${version_string}".py
    # build!
    echo "Laucnhing py2app..."
    python setup_py2app_"${version_string}".py py2app
    rm setup_py2app_"${version_string}".py
    # now, for some serious manually-powered stripping of unecessary files
    echo "Manually stripping unnecessary PyQt5 components..."
    app_folder_pyqt5_root='dist/Openroast '"${version_string}"'.app/Contents/Resources/lib/python3.5/PyQt5'
    app_folder_matplotlib_root='dist/Openroast '"${version_string}"'.app/Contents/Resources/lib/python3.5/matplotlib'
    # ----------
    # pkgs/PyQt5
    # ----------
    # need pkgs/PyQt5/__init__.py - don't remove
    rm -rf "${app_folder_pyqt5_root}"/_QOpenGL*
    rm -rf "${app_folder_pyqt5_root}"/pylupdate*
    rm -rf "${app_folder_pyqt5_root}"/pyrcc*
    rm -rf "${app_folder_pyqt5_root}"/Qt.so
    rm -rf "${app_folder_pyqt5_root}"/QtBluetooth.so
    # need pkgs/PyQt5/QtCore.so - don't remove
    rm -rf "${app_folder_pyqt5_root}"/QtD*
    # need pkgs/PyQt5/QtGui.pyd - don't remove
    rm -rf "${app_folder_pyqt5_root}"/QtH*
    rm -rf "${app_folder_pyqt5_root}"/QtL*
    # need rm -rf "${app_folder_pyqt5_root}"/QtMacExtras*
    rm -rf "${app_folder_pyqt5_root}"/QtMultimedia*
    rm -rf "${app_folder_pyqt5_root}"/QtN*
    rm -rf "${app_folder_pyqt5_root}"/QtO*
    rm -rf "${app_folder_pyqt5_root}"/QtP*
    rm -rf "${app_folder_pyqt5_root}"/QtQ*
    rm -rf "${app_folder_pyqt5_root}"/QtS*
    rm -rf "${app_folder_pyqt5_root}"/QtT*
    rm -rf "${app_folder_pyqt5_root}"/QtWeb*
    # need pkgs/PyQt5/QtWidgets.so - don't remove
    rm -rf "${app_folder_pyqt5_root}"/QtX*
    # # -----------------
    # # pkgs/PyQt5/Qt/bin
    # # -----------------
    rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtB*
    rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtCLucene.framework
    rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtConcurrent.framework
    # need pkgs/PyQt5/Qt5Core.dll - don't remove
    rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtD*
    # need pkgs/PyQt5/Qt5Gui.dll - don't remove
    rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtH*
    rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtL*
    # need rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtMacExtras*
    rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtMultimedia*
    rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtN*
    rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtO*
    # need rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtPrintSupport*
    rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtPositioning*
    rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtQ*
    rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtS*
    rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtT*
    rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtWeb*
    # # need pkgs/PyQt5/Qt5Widgets.dll - don't remove
    rm -rf "${app_folder_pyqt5_root}"/Qt/lib/QtX*
    # ------------------------------------
    # Whole Qt5 folders of 'don't need'...
    # ------------------------------------
    rm -rf "${app_folder_pyqt5_root}"/Qt/qml
    rm -rf "${app_folder_pyqt5_root}"/Qt/translations
    # ---------------------------------------
    # second copy of matplotlib data mpl-data
    # ---------------------------------------
    rm -rf "${app_folder_matplotlib_root}"/mpl-data

    # Create DMG for distribution
    echo "Creating DMG..."
    ./build_tools/create-dmg/create-dmg \
--window-pos 100 100 \
--window-size 400 200 \
--icon-size 100 \
--icon 'Openroast '"${version_string}"'.app' 100 100 \
--app-drop-link 300 100 \
'./dist/Openroast '"${version_string}"' Installer.dmg' \
dist \
/
    rm -rf 'dist/Openroast '"${version_string}"'.app' 
    echo "make_install done."
fi