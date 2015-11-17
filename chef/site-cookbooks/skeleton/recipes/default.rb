skeleton = node[:skeleton]
app_user = skeleton[:app_user]
app_name = skeleton[:app_name]
db = skeleton[:db]
python_env = skeleton[:python][:virtualenv]
site_dir = skeleton[:site_dir]
log_dir = skeleton[:log_dir]
script_dir = "#{site_dir}/scripts"
socket_dir = skeleton[:socket_dir]
static_dir = "#{site_dir}/app/static"
uploads_dir = "#{static_dir}/uploads"

include_recipe 'apt'
include_recipe 'nginx'
include_recipe 'python'
include_recipe 'postgresql::client'
include_recipe 'redisio'
include_recipe 'redisio::install'
include_recipe 'redisio::enable'

if db[:host] == 'localhost'

    include_recipe 'postgresql::server'

    postgresql_user db[:username] do
        password db[:password]
    end

    postgresql_database db[:database] do
        owner db[:username]
    end
end

pkgs = [
    "libjpeg-dev",
    "zlib1g-dev",
    "libpng12-dev",
    "libpq-dev",
    "libffi-dev",
]

pkgs.each do |pkg|
    package pkg do
        action :install
    end
end

user app_user do
    home "/home/#{app_user}"
    shell '/bin/bash'
    supports :manage_home => true
    action :create
end

[log_dir, script_dir, python_env, socket_dir].each do |dir|
    directory dir do
        owner app_user
        group app_user
        action :create
        recursive true
    end
end

python_virtualenv python_env do
    action :create
    group app_user
    owner app_user
end

#template "#{site_dir}/config/db.json"

template "#{site_dir}/config/uwsgi.ini" do
    owner app_user
    group app_user
end

template "#{site_dir}/config/main.py" do
    owner app_user
    group app_user
end

template "#{script_dir}/set_env.sh" do
    owner app_user
    group app_user
    mode '755'
end

template "#{script_dir}/skeleton.sh" do
    owner app_user
    group app_user
    mode '755'
end

template "/etc/init/#{app_name}.conf" do
    source 'skeleton-upstart.erb'
end

template "#{script_dir}/worker.sh" do
    source 'worker.sh.erb'
    mode '755'
end

template "/etc/init/#{app_name}_worker.conf" do
    source 'worker-upstart.erb'
end

#template "#{site_dir}/run.py" do
#    owner app_user
#end

template "#{site_dir}/worker.py" do
    source 'worker.py.erb'
    owner app_user
    group app_user
end

# script to excute i18n in Flask
#template "#{script_dir}/tr_compile.sh" do
#    source 'tr_compile.sh.erb'
#    mode '755'
#end

#template "#{script_dir}/tr_update.sh" do
#    source 'tr_update.sh.erb'
#    mode '755'
#end

#template "#{script_dir}/tr_ini.sh" do
#    source 'tr_ini.sh.erb'
#    mode '755'
#end


template "#{script_dir}/deploy.sh" do
    source 'deploy.sh.erb'
    mode '755'
end

#show stat script
template "#{script_dir}/monitor.sh" do
    source 'monitor.sh.erb'
    mode '755'
end

template "#{site_dir}/alembic.ini" do
    source 'alembic.ini.erb'
    mode '755'
end

service app_name do
    provider Chef::Provider::Service::Upstart
    action [:enable, :start, :restart]
end

service "#{app_name}_worker" do
    provider Chef::Provider::Service::Upstart
    action [:enable, :start, :restart]
end

bash 'Update db schema' do
    cwd "#{site_dir}"
    code <<-EOH
        . scripts/set_env.sh
        alembic upgrade head
    EOH
end

# Nginx
template "/etc/nginx/sites-available/#{app_name}" do
    source 'nginx-site.erb'
    notifies :restart, 'service[nginx]'
end

nginx_site app_name do
    action :enable
end

nginx_site 'default' do
    action :disable
end

template "/etc/logrotate.d/#{app_name}" do
    source 'logrotate.erb'
end

dirs = [
    "#{uploads_dir}",
    "#{uploads_dir}/photo",
    "#{uploads_dir}/photo/origin",
    "#{uploads_dir}/photo/crop",
    "#{uploads_dir}/photo/large",
    "#{uploads_dir}/photo/medium",
    "#{uploads_dir}/photo/small",
]

dirs.each do |component|
    the_dir = "#{component}"
    bash "Create folders #{the_dir}" do
        code <<-EOH
            mkdir -p #{the_dir}
            chown -R #{app_user} #{the_dir}
            chgrp -R www-data #{the_dir}
            chmod -R g+rw #{the_dir}
            find #{the_dir} -type d | xargs chmod g+x
        EOH
    end
end