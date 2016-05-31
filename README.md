# Ansible Playbook for Airflow

## Introduction

Airflow expresses relationships between jobs as a Directed Acyclic Graph. It lets you set dependencies for jobs, so they
only run when their dependencies complete successfully. It also lets you define retry logic for jobs, monitor job
completion/errors, view job runs in a web UI, and more. Full docs [here](https://pythonhosted.org/airflow/).


## Configuring

Change the default production inventory for the playbook (`playbook/inventories/production`) to whichever host you want
to deploy Airflow to. Update `playbook/vars/airflow-dev.yml` and `playbook/vars/airflow-prod.yml` with your choice of
credentials/settings (mysql users, fernet keys, etc.).  


## Running the App in Dev

`vagrant up`, then visit **192.168.33.11** in your browser to see the Airflow web interface.

Airflow consists of 3 Python services: a scheduler, a set of workers, and a web app.  The scheduler determines what
tasks airflow should perform when (i.e. what to monitor), the workers actually perform the tasks, and the web server
gives you a web interface where you can view the statuses of all your jobs.

The logs for these services are located at:

    $AIRFLOW_HOME/airflow-worker.log
    $AIRFLOW_HOME/airflow-scheduler.log
    $AIRFLOW_HOME/airflow-webserver.log

And you can start/stop/restart any of them with:

    $ sudo service airflow-worker {start|stop|restart}
    $ sudo service airflow-scheduler {start|stop|restart}
    $ sudo service airflow-webserver {start|stop|restart}

You can also start/stop services with the `dev-runner.sh` script, run `./runner.sh -h` for usage.

The DAG definitions can be found in the `workflows` dir.


## Running the App in Prod

Run the playbook against the prod inventory:

    $ ansible-playbook main.yml -i playbook/inventories/production

Deploy the airflow dir via your favourite means to `$AIRFLOW_HOME` on the prod server.  For a quick MVP, if you don't
want to use a more formal build/deploy tool, you can just tar and scp the dir up to the server.  Restart Airflow
services, and the jobs should run.
