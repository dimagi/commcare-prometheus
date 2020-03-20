require 'serverspec'
set :backend, :exec

describe service('prometheus') do
  it { should be_enabled }
  it { should be_running }
end

describe port(9090) do
  it { should be_listening }
end

