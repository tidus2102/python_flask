# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    config.vm.box = 'precise32'
    config.vm.box_url = 'http://boxes.cogini.com/precise32.box'

    # Install vagrant-trigger plugin if not installed
    unless Vagrant.has_plugin?('vagrant-triggers')
        # Bail out on failure so we don't get stuck in an infinite loop.
        system('vagrant plugin install vagrant-triggers') || exit!

        # Relaunch Vagrant so the new plugin(s) are detected.
        # Exit with the same status code.
        exit system('vagrant', *ARGV)
    end

    config.trigger.before [:reload, :up], stdout: true do
        SYNCED_FOLDER = ".vagrant/machines/default/virtualbox/synced_folders"
        begin
            info "Trying to delete #{SYNCED_FOLDER}"
            File.delete(SYNCED_FOLDER)
        rescue StandardError => e
            warn "Could not delete #{SYNCED_FOLDER}."
            warn e.inspect
        end
    end

    config.vm.network :forwarded_port, guest: 80, host: 9990
    config.vm.network :forwarded_port, guest: 22, host: 9991, id: "ssh", auto_correct: true

    apt_cache = './apt-cache'
    FileUtils.mkpath "#{apt_cache}/partial"

    chef_cache = '/var/chef/cache'

    shared_folders = {
        apt_cache => '/var/cache/apt/archives',
        './.cache/chef' => chef_cache,
    }

    config.vm.provider :virtualbox do |vb|

        #vb.gui = true

        shared_folders.each do |source, destination|
            FileUtils.mkpath source
            config.vm.synced_folder source, destination
            vb.customize ['setextradata', :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/#{destination}", '1']
        end

        vb.customize ['setextradata', :id, 'VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root', '1']
    end

    config.vm.provision :chef_solo do |chef|

        chef.custom_config_path = "Vagrantfile.chef"
        chef.provisioning_path = chef_cache

        chef.cookbooks_path = [
            'chef/chef-cookbooks',
            'chef/site-cookbooks',
        ]

        chef.json = {
            :skeleton => {
                :env => 'local',
                :server_name => 'localhost',
                :endpoint => 'localhost:9990',
                :app_user => 'vagrant',
                :app_name => 'skeleton',
                :log_dir => '/vagrant/logs',
                :pid_dir => '/tmp/skeleton',
                :site_dir => '/vagrant',
                :socket_dir => '/tmp/skeleton',
                :db => {
                    :password => 'vagrant',
                },
                :email => {
                    :admin => 'admin@vagrant.local',
                    :sender => 'sender@vagrant.local',
                },
                :blocked_keywords => [
                    "/phpMyAdmin",
                    "/mysqladmin",
                    "/muieblackcat",
                    "/manager/html",
                    "/test",
                    "/proxy.txt",
                    ".php",
                ],
            },

            # Vagrant attributes
            :users => [
                {
                    :name => "vagrant",
                    :ssh => true,
                    :sudo => true,
                    :admin => true,
                }
            ],
            :nginx => {
                :client_max_body_size => '100M',
                :sendfile => 'off',
            },
            :postgresql => {
                :client_auth => [
                    {
                        :type => 'local',
                        :database => 'all',
                        :user => 'all',
                        :auth_method => 'trust',
                    }
                ],
                :version => '9.3'
            }
        }

        chef.add_recipe 'vagrant'
    end
end
