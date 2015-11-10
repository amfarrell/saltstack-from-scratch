Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.box_url = "ubuntu/trusty64"

  config.vm.define :frodo , primary: true do |machine|
    machine.vm.provider :virtualbox do |v|
      v.name = "frodo"
    end

    machine.vm.hostname = "frodo"
    machine.vm.synced_folder "./frodo_vagrant", "/vagrant", :create => true

    machine.vm.network :private_network, ip: "10.10.10.100"
    machine.vm.network :forwarded_port, guest: 80, host: 8001
    machine.vm.network :forwarded_port, guest: 8080, host: 8081
    machine.vm.provision :hostmanager
  end

  config.vm.define :samwise do |machine|
    machine.vm.provider :virtualbox do |v|
      v.name = "samwise"
    end

    machine.vm.hostname = "samwise"
    machine.vm.synced_folder "./samwise_vagrant", "/vagrant", :create => true

    machine.vm.network :private_network, ip: "10.10.10.101"
    machine.vm.network :forwarded_port, guest: 80, host: 8002
    machine.vm.network :forwarded_port, guest: 8080, host: 8082
    machine.vm.provision :hostmanager
  end

  config.vm.provision :hostmanager
end
