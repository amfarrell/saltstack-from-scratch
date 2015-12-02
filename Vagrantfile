Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.box_url = "ubuntu/trusty64"

  config.vm.define :arthur , primary: true do |machine|
    machine.vm.provider :virtualbox do |v|
      v.name = "arthur"
    end

    machine.vm.hostname = "arthur"
    machine.vm.synced_folder "./arthur_vagrant", "/vagrant", :create => true

    machine.vm.network :private_network, ip: "10.10.10.100"
    machine.vm.network :forwarded_port, guest: 80, host: 8001
    machine.vm.network :forwarded_port, guest: 8080, host: 8081
    machine.vm.provision :hostmanager
  end

  config.vm.define :galahad do |machine|
    machine.vm.provider :virtualbox do |v|
      v.name = "galahad"
    end

    machine.vm.hostname = "galahad"
    machine.vm.synced_folder "./galahad_vagrant", "/vagrant", :create => true

    machine.vm.network :private_network, ip: "10.10.10.101"
    machine.vm.network :forwarded_port, guest: 80, host: 8002
    machine.vm.network :forwarded_port, guest: 8080, host: 8082
    machine.vm.provision :hostmanager
  end

  config.vm.provision :hostmanager
end
