master_vm_name = "arthur"
other_vm_name = "galahad"

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.box_url = "ubuntu/trusty64"

  config.vm.define master_vm_name , primary: true do |machine|
    machine.vm.provider :virtualbox do |v|
      v.name = master_vm_name
    end

    machine.vm.hostname = master_vm_name
    machine.vm.synced_folder "./#{master_vm_name}_vagrant", "/vagrant", :create => true

    machine.vm.network :private_network, ip: "10.10.10.100"
    machine.vm.network :forwarded_port, guest: 80, host: 8001
    machine.vm.network :forwarded_port, guest: 8080, host: 8081
    machine.vm.provision :hostmanager

    machine.vm.provision :shell, inline: "
      echo 'foo' >> /vagrant/#{master_vm_name}_synced
    "
  end

  config.vm.define other_vm_name do |machine|
    machine.vm.provider :virtualbox do |v|
      v.name = other_vm_name
    end

    machine.vm.hostname = other_vm_name
    machine.vm.synced_folder "./#{other_vm_name}_vagrant", "/vagrant", :create => true

    machine.vm.network :private_network, ip: "10.10.10.101"
    machine.vm.network :forwarded_port, guest: 80, host: 8002
    machine.vm.network :forwarded_port, guest: 8080, host: 8082
    machine.vm.provision :hostmanager

    machine.vm.provision :shell, inline: "
      echo 'foo' >> /vagrant/#{other_vm_name}_synced
    "
  end
end
