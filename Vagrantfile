Vagrant.configure("2") do |config|
  # Specify the RHEL 9 box
  config.vm.box = "generic/rocky9" # Change if using another provider

  # Set up the VM
  config.vm.hostname = "rocky9-vm"
  config.vm.network "private_network", type: "dhcp"

  # Customize VM resources
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = 2
  end

  # Enable SSH
  config.ssh.insert_key = false

  # Provisioning (Optional: Install packages)
  config.vm.provision "shell", inline: <<-SHELL
    sudo dnf update -y
    sudo dnf install -y ansible-core
    sudo dnf install -y ansible
    sudo dnf install -y python3-jmespath
  SHELL

  config.vm.provision "shell", inline: <<-SHELL
    sudo mkdir -p /fs/u02/apps_ux /fs/u02/apps_data /fs/u02/sw_ux
    sudo touch /fs/u02/apps_ux/range:8000-8080
    sudo chmod -R 775 /fs/u02
    sudo ln -s /fs/u02/apps_data /apps_data
    sudo ln -s /fs/u02/apps_ux /apps_ux
    sudo ln -s /fs/u02/sw_ux /sw_ux
    sudo groupadd -g 778 wwwadm
    sudo useradd -u 778 -g 778 -c "apache user" -m -d /fs/u02/apps_ux/wwwadm -s /sbin/nologin wwwadm
    sudo useradd -u 779 -g 778 -c "apache service" -m -d /fs/u02/apps_ux/wwwsvr -s /sbin/nologin wwwsvr
    sudo chown wwwadm:wwwadm /fs/u02 /fs/u02/apps_ux /fs/u02/apps_data /fs/u02/sw_ux
    sudo -i echo "umask 022" >> /apps_ux/wwwadm/.bashrc
    sudo -i echo "umask 022" >> /apps_ux/wwwsvr/.bashrc
    sudo sed -i -- 's/PasswordAuthentication no/#PasswordAuthentication no/g' /etc/ssh/sshd_config
    sudo sed -i -- 's/#PasswordAuthentication yes/PasswordAuthentication yes/g' /etc/ssh/sshd_config
    sudo systemctl restart sshd
    sudo -i echo "vagrant ALL=(wwwadm) NOPASSWD: ALL" >> /etc/sudoers
    sudo -i echo "vagrant ALL=(wwwsvr) NOPASSWD: ALL" >> /etc/sudoers
    sudo loginctl enable-linger wwwsvr
    sudo loginctl user-status wwwsvr || echo "Lingering enabled, systemd user session will start on demand."
    sudo mkdir -p /fs/u02/apps_ux/wwwsvr/.config/systemd/user
    sudo chown wwwsvr:wwwadm /fs/u02/apps_ux/wwwsvr/.config /fs/u02/apps_ux/wwwsvr/.config/systemd /fs/u02/apps_ux/wwwsvr/.config/systemd/user
    sudo chmod 775 /fs/u02/apps_ux/wwwsvr/.config /fs/u02/apps_ux/wwwsvr/.config/systemd /fs/u02/apps_ux/wwwsvr/.config/systemd/user
    sudo chmod 755 /fs/u02/apps_ux/wwwsvr
  SHELL

end
