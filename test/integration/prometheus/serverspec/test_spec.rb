require 'serverspec'
set :backend, :exec

config_check_command = '/usr/local/bin/promtool  check config /etc/prometheus/prometheus.yml'

describe command (config_check_command) do
  its (:exit_status) {should eq 0}
end

describe service('prometheus') do
  it { should be_enabled }
  it { should be_running }
end

describe port(9090) do
  it { should be_listening }
end

