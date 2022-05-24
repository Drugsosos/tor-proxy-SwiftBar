#!/bin/zsh

# Get OS
unameOut="$(uname -s)"
case "${unameOut}" in
    Darwin*)
      machine=Mac
      ;;
    Linux*)
      machine=Linux
      ;;
    *)
      machine="UNKNOWN:${unameOut}"
esac

# Exit if not Mac OS
if [ ! "$machine" = "Mac" ]; then
  echo "$unameOut not supported"
  exit 0
fi

# Check brew is installed
if [ -z "$(command -v brew)" ]; then
  echo "Install brew? [enter]"
  read -r -s -n 1 brew_status
  if [[ $brew_status = "" ]]; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi
fi

# Check python3.10 is installed
if [ -z "$(command -v python3.10)" ]; then
  echo "Install python3.10? [enter]"
  read -r -s -n 1 python_status
  if [[ $python_status = "" ]]; then
    brew install python@3.10
  fi
fi

# Check tor is installed
if [ -z "$(command -v tor)" ]; then
  echo "Install tor? [enter]"
  read -r -s -n 1 tor_status
  if [[ $tor_status = "" ]]; then
    brew install tor
  fi
fi

# Check obfs4proxy is installed
if [ -z "$(command -v obfs4proxy)" ]; then
  echo "Install obfs4proxy? [enter]"
  read -r -s -n 1 obfs_status
  if [[ $obfs_status = "" ]]; then
    brew install obfs4proxy
  fi
fi

# Edit torrc
echo "Edit torrc (tor configuration file)? [enter]"
read -r -s -n 1 edit_torrc
if [[ $edit_torrc = "" ]]; then
  torrc_location="/opt/homebrew/etc/tor/torrc"

  if [ -f "$torrc_location" ]; then
    rm -rf "$torrc_location"
  fi

  obfs_location="$(which obfs4proxy)"

  {
    echo "RunAsDaemon 1"
    echo "UseBridges 1"
    echo "ClientTransportPlugin obfs2,obfs3,obfs4,scramblesuit exec $obfs_location"
    echo "# Temporary"
    echo "Bridge obfs4 185.177.207.191:8443 F25CC9227A749C5603E7D3799933026B369A5EF0 cert=LSHlzHPcfHw4mBbNz/H0NL2pKY/FiuVLVhJZ0/qxT67Ho6U6XbA7BNPSUfWDn7uXUSDndg iat-mode=0"
  } >> "$torrc_location"

  echo "Add your own bridges in\n$torrc_location"
  sleep 5
fi

# Exit
exit 1