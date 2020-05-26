require 'serverspec'
set :backend, :exec

describe service('loki_server') do
  it { should be_enabled }
  it { should be_running }
end

describe service('promtail') do
  it { should be_enabled }
  it { should be_running }
end
