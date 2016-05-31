#!/bin/sh

password_hash=$(python -c "from cryptography.fernet import Fernet; \
  print Fernet('{{ airflow_fernet_key }}').encrypt('{{ item.password }}')")

mysql --user={{ mysql_airflow_user }} \
  --password={{ mysql_airflow_password }} \
  --database={{ db_name }} \
  --execute="insert into connection select \
    null, \
    '{{ item.conn_id }}', \
    '{{ item.conn_type }}', \
    '{{ item.host }}', \
    '{{ item.schema }}', \
    '{{ item.login }}', \
    '$password_hash', \
    '{{ item.port }}', \
    null, \
    1, \
    0 \
    from dual where not exists (select conn_id from connection where conn_id = '{{ item.conn_id }}');"
