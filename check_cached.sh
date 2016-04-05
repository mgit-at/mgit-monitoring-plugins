#!/bin/bash
# transparent cache for nagios checks
# Author: Christoph Hack <chack@mgit.at>
# (c) 2016 by mgIT
readonly CACHEFILE="/run/check_cached"
readonly CACHETIME="30" # 30min

function usage {
  echo "Usage: check_cached [-t CACHE_TIME] <command>"
  exit 1
}

function main {
  local cachetime="$CACHETIME"
  if [[ "$1" == "-t" ]]; then
    cachetime="$2"
    if [[ -z "$cachetime" ]]; then
       usage
    fi
    shift 2
  fi
  if [[ "$#" < 1 ]]; then
    usage
  fi

  local dir="$(realpath "$1")"
  local key="$(printf "%s\0" "$@" | sha256sum | head -c 16)"
  local cache="${CACHEFILE}.${key}"

  find "$cache" -mmin "-$CACHETIME" &> /dev/null
  if [[ "$?" == 0 ]]; then
    local rval="$(head -n 1 "$cache")"
    local out="$(tail -n +2 "$cache")"
    echo "$out"
    exit "$rval"
  fi
  local out;
  local rval;

  out=$(eval "$@")
  rval="$?"

  echo -e "$rval\n$out" > "$cache"

  echo "$out"
  exit "$rval"
}
main "$@"
