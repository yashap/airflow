#!/usr/bin/env bash

# Settings
VAGRANT_DIR="."

# Definitions
stop_airflow() {
  (cd "$VAGRANT_DIR" && vagrant ssh -c "
    sudo service airflow-webserver stop;
    sudo service airflow-scheduler stop;
    sudo service airflow-worker stop;
  ")
}

start_airflow() {
  (cd "$VAGRANT_DIR" && vagrant ssh -c "
    sudo service airflow-worker start;
    sudo service airflow-scheduler start;
    sudo service airflow-webserver start;
  ")
}

reset_db() {
  (cd "$VAGRANT_DIR" && yes | vagrant ssh -c "airflow resetdb")
}

vagrant_up() {
  (cd "$VAGRANT_DIR" && vagrant up)
}

vagrant_provision() {
  (cd "$VAGRANT_DIR" && vagrant provision)
}

vagrant_ssh() {
  (cd "$VAGRANT_DIR" && vagrant ssh)
}

main() {
  vagrant_up

  if [ "$CLEAN" ]; then
    stop_airflow
    reset_db
    start_airflow
  elif [ "$START" ]; then
    start_airflow
  elif [ "$STOP" ]; then
    stop_airflow
  elif [ "$RESTART" ]; then
    stop_airflow
    start_airflow
  fi

  if [ "$SSH" ]; then
    vagrant_ssh
  fi
}

# Parse command line args
while getopts ":csprh" opt; do
  case "$opt" in
    c) CLEAN=true;;
    s) START=true;;
    p) STOP=true;;
    r) RESTART=true;;
    h)
      echo "Usage:
      -c stop airflow, clear airflow's db, start airflow
      -s start all airflow service
      -p stop all airflow service
      -r restart all airflow services"
      exit 0
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

# Main run
main
