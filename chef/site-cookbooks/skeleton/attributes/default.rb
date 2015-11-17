default[:skeleton][:app_name] = 'skeleton'
default[:skeleton][:app_user] = 'skeleton'

default[:skeleton][:db][:driver] = 'postgresql'
default[:skeleton][:db][:host] = 'localhost'
default[:skeleton][:db][:database] = 'skeleton'
default[:skeleton][:db][:username] = 'skeleton'

default[:skeleton][:port] = 8125
default[:skeleton][:stat_port] = 24125
default[:skeleton][:server_port] = 80
default[:skeleton][:secret_key] = 'dHKEf1IXUV6pHULHaAOUaL0podQzs9ubg'

default[:skeleton][:python][:virtualenv] = '/home/skeleton/.virtualenvs/skeleton'
default[:skeleton][:has_loadbalancer] = false
default[:skeleton][:endpoint] = ''
default[:skeleton][:protocol] = 'http://'

# This is more like a constant. Don't change it, as v0.11.12 has error

#environment: local or dev or prod
default[:skeleton][:env] = 'dev'

#emails
default[:skeleton][:emails][:admin] = 'tidus2102@gmail.com'
default[:skeleton][:emails][:mandrill][:api_key] = ''

#email to send error
default[:skeleton][:emails][:errors] = [
    # 'error@skeleton.com',
]
default[:skeleton][:emails][:debug] = false

default[:skeleton][:remote_console] = {
    # :port => 7777,
    # :passwd_file => "passwd"
}

default[:skeleton][:debug] = true

#default[:skeleton][:apns] = {
#    :sandbox => false,
#    :cert_file => "config/apns.pem",
#    :debug => false,
#}

default[:skeleton][:gcm][:api_key] = "AIzaSyCRTK18MJ4mmOwYe_PorRFAdd26oQKH_Xc"

# Redis config
default[:redisio][:default_settings][:logfile] = '/var/log/redis.log'
default[:redisio][:job_control] = 'upstart'