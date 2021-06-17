#!/usr/bin/env bash

###
# This script allows you to install any Docker image and run it on your local environment.
#
# To install Rasa, please invoke the script as follows:
#
# ./install-docker-image.sh --image rasa/rasa:1.10.1-full && source .bashrc && rm .bashrc
#
# Right after having run the script you should be able to use Rasa in your current terminal:
# 
# rasa --version
#
# Follow the printed instructions in order to make the changes permanent.
###

set -e

function print_help {
  echo "Usage: `basename "$0"` --image [docker_image|docker_image/version]"
}

function print_alias {
  echo ""
  echo "== All done! =="
  echo "You can run $1 in your current terminal session."
  echo "To make it permanent, please append this line:"
  echo ""
  echo $2
  echo ""
  echo "to your shell configuration file:"
  echo "  Bash – ~/.bashrc"
  echo "  ZSH – ~/.zshrc"
  echo "  Fish – ~/.config/fish/config.fish"
}

function create_temp_alias {
  local_bashrc="$(pwd)/.bashrc"
  image_alias="docker container run --rm -it -v \$(pwd):/app --user 1000:1000 $1/$2"
  alias_cmd="alias $1=\"${image_alias}\""
  echo "${alias_cmd}" >> "${local_bashrc}"
  print_alias $1 "${alias_cmd}" 
}

image=""
version=""

while (( "$#" )); do
  case "$1" in
    --help|-h)
      print_help
      exit 0
      ;;
    --image)
      IFS='/'
      read -a arr <<<"$2"
      if [[ "${#arr[@]}" == 0 ]]; then
        print_help
        exit 1
      fi  
      image="${arr[0]}"
      version="${arr[1]}"
      shift 2
      ;;
    *)
      print_help
      exit 1
  esac
done

if [ -z "${version}" ]; then
  echo "No version specified, using the latest"
  version="latest"
fi

# download the requested image
docker pull "${image}/${version}"

# create an alias
create_temp_alias "${image}" "${version}"
