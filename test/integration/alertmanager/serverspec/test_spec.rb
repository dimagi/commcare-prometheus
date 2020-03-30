require 'serverspec'
set :backend, :exec

config_check_command = '/usr/local/bin/amtool  check-config /etc/alertmanager/alertmanager.yml'

describe command (config_check_command) do
  its (:exit_status) {should eq 0}
end

describe service('alertmanager') do
  it { should be_enabled }
  it { should be_running }
end

describe port(9093) do
  it { should be_listening }
end
