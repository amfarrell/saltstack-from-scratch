master_vm_name = "arthur"
other_vm_name = "galahad"
minion_names = "'#{master_vm_name}' '#{other_vm_name}'"

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.box_url = "ubuntu/trusty64"

  config.vm.define master_vm_name, primary: true do |machine|
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
      add-apt-repository ppa:saltstack/salt
      apt-get update -y
      apt-get install salt-minion salt-master -y

      cp /vagrant/salt/master /etc/salt/master
      service salt-master restart

      echo '#{master_vm_name}' > /etc/salt/minion_id
      if [ -z \"$(grep 'master: arthur' /vagrant/salt/minion)\" ] ; then
        echo 'master: #{master_vm_name}' >> /vagrant/salt/minion
      fi
      cp /vagrant/salt/minion /etc/salt/minion
      service salt-minion restart


      echo \"salt '*' state.sls ag  > /vagrant/enforce-states.log\" > /vagrant/enforce-states
      chmod +x /vagrant/accept-keys
      CALLBACK_SCRIPT='/vagrant/enforce-states' /vagrant/accept-keys #{minion_names} > /vagrant/accept-keys.log &
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
      add-apt-repository ppa:saltstack/salt
      apt-get update -y
      apt-get install salt-minion -y

      echo '#{other_vm_name}' > /etc/salt/minion_id
      if [ -z \"$(grep 'master: arthur' /vagrant/salt/minion)\" ] ; then
        echo 'master: #{master_vm_name}' >> /vagrant/salt/minion
      fi
      cp /vagrant/salt/minion /etc/salt/minion
      service salt-minion restart

      chmod +x /vagrant/send-key
      /vagrant/send-key > /vagrant/send-key.log &
    "
  end



  config.vm.provision :hostmanager
end
