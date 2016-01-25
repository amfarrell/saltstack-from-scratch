require 'yaml'

master_vm_name = "arthur"
other_vm_name = "galahad"
minion_names = "'#{master_vm_name}' '#{other_vm_name}'"

begin
  file = File.open('./digital_ocean_data.yaml', 'r')
  data = YAML.load(file.read())
  digital_ocean_token = data['token']
  ssh_key_path = data['ssh_key_path']
rescue SystemCallError
  $stderr.print("Create a file named 'digital_ocean_data.yaml' in the same directory as Vagrantfile.\n
                 Put your digital ocean API token and the path to your ssh key in it.\n")
end



Vagrant.configure('2') do |config|
  config.vm.box = 'digital_ocean'
  config.vm.box_url = "https://github.com/smdahlen/vagrant-digitalocean/raw/master/box/digital_ocean.box"

  config.vm.define master_vm_name, primary: true do |machine|
    machine.vm.provider :digital_ocean do |provider, override|
      provider.name = master_vm_name
      provider.token = digital_ocean_token
      provider.image = 'ubuntu-14-04-x64'
      provider.region = 'nyc1'
      provider.size = '512mb'

      override.ssh.private_key_path = ssh_key_path
    end
    machine.vm.synced_folder "./#{master_vm_name}_vagrant", "/vagrant", :create => true

    machine.vm.provision :shell, inline: "
        add-apt-repository ppa:saltstack/salt
        apt-get update -y
        apt-get install salt-minion salt-master -y

        cp /vagrant/salt/master /etc/salt/master
        service salt-master restart

        echo '#{master_vm_name}' > /etc/salt/minion_id
        if [ -z \"$(grep 'master: #{master_vm_name}' /vagrant/salt/minion)\" ] ; then
        echo 'master: #{master_vm_name}' >> /vagrant/salt/minion
        fi
        cp /vagrant/salt/minion /etc/salt/minion
        service salt-minion restart

        echo \"salt '*' state.highstate  > /vagrant/enforce-states.log\" > /vagrant/enforce-states
        chmod +x /vagrant/accept-keys
        CALLBACK_SCRIPT='/vagrant/enforce-states' /vagrant/accept-keys #{minion_names} > /vagrant/accept-keys.log &

        echo '\n'
        echo \"#{master_vm_name} set up at http://$(curl http://169.254.169.254/latest/meta-data/public-ipv4 2> /dev/null )/admin\"
        echo '\n'
    "
  end

  config.vm.define other_vm_name do |machine|
    machine.vm.provider :digital_ocean do |provider, override|
      provider.name = other_vm_name
      provider.token = digital_ocean_token
      provider.image = 'ubuntu-14-04-x64'
      provider.region = 'nyc1'
      provider.size = '512mb'

      override.ssh.private_key_path = ssh_key_path
    end
    machine.vm.synced_folder "./#{other_vm_name}_vagrant", "/vagrant", :create => true

    machine.vm.provision :shell, inline: "
      add-apt-repository ppa:saltstack/salt
      apt-get update -y
      apt-get install salt-minion -y

      echo '#{other_vm_name}' > /etc/salt/minion_id
      if [ -z \"$(grep 'master: #{master_vm_name}' /vagrant/salt/minion)\" ] ; then
      echo 'master: #{master_vm_name}' >> /vagrant/salt/minion
      fi
      cp /vagrant/salt/minion /etc/salt/minion
      service salt-minion restart

      chmod +x /vagrant/send-key
      /vagrant/send-key > /vagrant/send-key.log &

      echo '\n'
      echo \"#{other_vm_name} set up at http://$(curl http://169.254.169.254/latest/meta-data/public-ipv4 2> /dev/null )/admin\"
      echo '\n'
    "
  end
  config.vm.provision :hostmanager
end
