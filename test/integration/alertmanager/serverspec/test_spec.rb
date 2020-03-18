require 'serverspec'
set :backend, :exec

describe package('alertmanager') do
    it { should be_installed }
  end

describe service('alertmanager') do
  it { should be_enabled }
  it { should be_running }
end

describe port(9100) do
  it { should be_listening }
end
