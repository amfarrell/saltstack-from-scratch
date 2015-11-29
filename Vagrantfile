Vagrant.configure("2") do |config|
  config.vm.box = "dummy"

  config.vm.provider :aws do |aws, override|
    aws.region = "us-west-2"
    aws.instance_type = "m3.medium"
    aws.access_key_id = ENV['AWS_KEY_ID']
    aws.secret_access_key = ENV['AWS_KEY_SECRET']
    #aws.session_token = "SESSION TOKEN"
    aws.keypair_name = "salt-demo"
    aws.ami = "ami-534d5d32"
    aws.security_groups = ["default", "vagrant"]
    aws.tags = {
        'created_from'=> 'Vagrant'
    }

    override.ssh.username = "ubuntu"
    override.ssh.private_key_path = "/Users/afarrell/projects/saltmarsh/salt-demo.pem"
  end
end
