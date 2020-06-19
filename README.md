# Ansible Role:  Prometheus , Grafana, Alertmanager, Exporter, Loki, Promtail setup for CommCare

## Testing locally

Requirements:
* Ruby (use [Ruby Version Manager](https://rvm.io/))
* Docker

1. `bundle install`

2. Run the tests

    ```
    kitchen converge
    kitchen verify
    ```
    Run the tests for particular component
    ```
    kitchen verify prometheus-node-exporter-ubuntu-1804
    ```

## How to use
1. Requiremets:
   *  ansible >= 2.9.4

2. installation
  please refer to this guide for [installation](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html)

3. Usage Example
```
- name: Prometheus RabbitMQ Exporter
  hosts: rabbitmq
  become: true
  tasks:
    - import_role:
        name: dimagi.commcare_prometheus.rabbitmq_exporter

```
4. Required variable
```
---
# It comes from external dependecies which we override in prometheus role but collection is not smart enough to get group_vars from repo so use dummy values
alertmanager_receivers:
- name: slack
  slack_configs:
  - send_resolved: true
    channel: '#alerts'
alertmanager_route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: slack
grafana_security:
  admin_user: 
  admin_password:
````
5. For other variables take a look at `group_vars/all.yml` and `default/main.yml` of every role.

## References

* [Alertmanager](https://prometheus.io/docs/alerting/configuration/)
* [Prometheus](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)
* [Grafana](https://grafana.com/)
* [Exporter](https://prometheus.io/docs/instrumenting/exporters/)
* [Loki](https://grafana.com/oss/loki/)
