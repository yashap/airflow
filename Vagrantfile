# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  BASEDIR = "#{`git rev-parse --show-toplevel`.strip}/playbook"
  EMAIL = `git config user.email`.strip

  config.vm.box = "ubuntu/trusty64"
  config.vm.network :private_network, ip: "192.168.33.11"
  config.vm.hostname = "airflow"

  config.ssh.username = "vagrant"
  config.ssh.password = "vagrant"

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", 6192]
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end

  config.vm.synced_folder "workflows", "/home/vagrant/airflow/workflows", create: true

  config.vm.provision :ansible do |ansible|
    ansible.playbook = "playbook/main.yml"
    ansible.inventory_path = "playbook/inventories/vagrant"
    ansible.extra_vars = { base_dir: BASEDIR, airflow_email_to: EMAIL }
  end
end
