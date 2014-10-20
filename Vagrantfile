# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box_url ='http://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_debian-7.4-i386_chef-provisionerless.box'
  config.vm.box ='wheezy'
  config.vm.provision "shell", path: "vagrant/provision/root.sh"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 8000, host: 9000
end