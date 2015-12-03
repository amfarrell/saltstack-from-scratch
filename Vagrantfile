["MASTER_NAME", "MINION_NAMES", "AWS_KEY_ID", "AWS_KEY_SECRET", "EC2_PEM_PATH"].each do |key|
    if not ENV.has_key?(key)
        raise "The environment variable #{key} must be defined."
    end
end

master_name = ENV.fetch('MASTER_NAME')
minion_names = ENV.fetch('MINION_NAMES').split

Vagrant.configure("2") do |config|
    config.vm.box = "dummy"

    config.vm.provider :aws do |aws, override|
        aws.region = "us-west-2"
        aws.instance_type = "m3.medium"
        aws.access_key_id = ENV.fetch('AWS_KEY_ID')
        aws.secret_access_key = ENV.fetch('AWS_KEY_SECRET')
        aws.keypair_name = "salt-demo"
        aws.ami = "ami-d24c5cb3"
        aws.tags = {
            'created_from'=> 'Vagrant'
        }
        override.ssh.username = "ubuntu"
        override.ssh.private_key_path = ENV.fetch("EC2_PEM_PATH")
    end

    config.vm.define master_name do |machine|
        machine.vm.provider :aws do |aws|
            aws.security_groups = ["default", "vagrant", "salt-master", "db"]
        end
        machine.vm.synced_folder "./arthur_vagrant", "/vagrant", :create => true
        machine.vm.provision :shell, inline: "
            add-apt-repository ppa:saltstack/salt
            apt-get update -y
            apt-get install salt-minion salt-master -y
            echo '#{master_name}' > /etc/salt/minion_id
            cp /vagrant/master /etc/salt/master
            cp /vagrant/minion /etc/salt/minion
            service salt-master restart
            service salt-minion restart
        "
    end

    minion_names.each do |hostname|
        config.vm.define hostname do |machine|
            machine.vm.provider :aws do |aws|
                aws.security_groups = ["default", "vagrant", "webserver"]
            end

            machine.vm.synced_folder "./galahad_vagrant", "/vagrant", :create => true
            machine.vm.provision :shell, inline: "
                add-apt-repository ppa:saltstack/salt
                apt-get update -y
                apt-get install salt-minion -y
                echo '#{hostname}' > /etc/salt/minion_id
                cp /vagrant/minion /etc/salt/minion
                service salt-minion restart
            "
        end
    end

    config.vm.provision :hostmanager
end
