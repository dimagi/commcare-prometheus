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

## References

* [Alertmanager](https://prometheus.io/docs/alerting/configuration/)
* [Prometheus](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)
* [Grafana](https://grafana.com/)
* [Exporter](https://prometheus.io/docs/instrumenting/exporters/)
* [Loki](https://grafana.com/oss/loki/)
