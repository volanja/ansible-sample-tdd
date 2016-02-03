require 'spec_helper'

describe package('mariadb-server') do
  it { should be_installed }
end

describe service('mariadb') do
  it { should be_enabled   }
  it { should be_running   }
end

describe port(3306) do
  it { should be_listening }
end

describe file('/etc/my.cnf') do
  it { should be_file }
end
