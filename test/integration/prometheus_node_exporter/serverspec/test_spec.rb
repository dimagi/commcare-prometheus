require 'serverspec'
set :backend, :exec

describe service('node_exporter') do
  it { should be_enabled }
  it { should be_running }
end

