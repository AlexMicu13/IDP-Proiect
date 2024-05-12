FROM grafana/grafana

RUN mkdir -p /var/lib/grafana
RUN mkdir -p /etc/grafana/provisioning

COPY ./data /var/lib/grafana
COPY ./grafana-provisioning/ /etc/grafana/provisioning
