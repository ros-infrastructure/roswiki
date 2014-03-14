node default {
   class { 'python':
        version => 'system',
        dev => true,
        virtualenv => true,
    }

    package {                                                                                                                                                                                                                                                                  
        'apache2': ensure => latest;                                                                                                                                                                                                                                   
        'libapache2-mod-wsgi': ensure => latest;
    }

    vcsrepo { '/var/www/wiki.ros.org/conf':
        ensure => present,
        provider => git,
        source => 'git://github.com/ros-infrastructure/roswiki.git',
        revision => 'conf',
    }    

    vcsrepo { '/var/www/wiki.ros.org/data/plugin':
        ensure => present,
        provider => git,
        source => 'git://github.com/ros-infrastructure/roswiki.git',
        revision => 'master',
    }    

    file { '/etc/apache2/sites-available/wiki.ros.org.conf':
        content => template('roswiki/wiki.ros.org.conf.erb'),
        require => Package['apache2'],
        notify => Service['apache2'],
    }

    file { '/etc/apache2/sites-enabled/wiki.ros.org.conf':
        ensure => 'link',
        target => '/etc/apache2/sites-available/wiki.ros.org.conf',
        notify => Service['apache2'],
        require => File['/etc/apache2/sites-available/wiki.ros.org.conf'],
    }

    file { '/etc/apache2/ports.conf':
        content => template('roswiki/ports.conf.erb'),
        require => Package['apache2'],
        notify => Service['apache2'],
    }

    file { '/etc/apache2/sites-enabled/000-default':
        ensure => absent,
        notify => Service['apache2'],
        require => Package['apache2'],
    }

    file { '/etc/apache2/mods-enabled/rewrite.load':
        ensure => 'link',
        target => '/etc/apache2/mods-available/rewrite.load',
        notify => Service['apache2'],
        require => Package['apache2'],
    }

    file { '/etc/apache2/mods-enabled/wsgi.load':
        ensure => 'link',
        target => '/etc/apache2/mods-available/wsgi.load',
        notify => Service['apache2'],
        require => Package['libapache2-mod-wsgi'],
    }

    service { 'apache2':
        ensure => running,
        require => Package['apache2'],
    }

    file { ['/var/www/wiki.ros.org/underlay', '/var/www/wiki.ros.org/underlay/pages',
        '/var/www/wiki.ros.org/data', '/var/www/wiki.ros.org/data/pages',
        '/var/log/apache2/wiki.ros.org', '/var/log/apache2/wiki.ros.org/access',
        '/var/log/apache2/wiki.ros.org/error']:
        owner => 'www-data',
        group => 'www-data',
        ensure => directory,
    }

    python::virtualenv { '/var/www/wiki.ros.org/venv':
        ensure => present,
        owner => 'www-data',
        group => 'www-data',
        require => [Vcsrepo['/var/www/wiki.ros.org/data/plugin'], File['/var/www/wiki.ros.org']],
    } 

    python::pip { 'newrelic':
        pkgname => 'newrelic',
        virtualenv => '/var/www/wiki.ros.org/venv',
        require => [Python::Virtualenv['/var/www/wiki.ros.org/venv'], Package['python-dev']],
        owner => 'www-data',
    }

    python::pip { 'moin':
        pkgname => 'moin',
        virtualenv => '/var/www/wiki.ros.org/venv',
        require => Python::Virtualenv['/var/www/wiki.ros.org/venv'],
        owner => 'www-data',
        install_args => ['--allow-external moin --allow-unverified moin'],
    }

    file { '/var/www/wiki.ros.org':
        ensure => directory,
        owner => www-data,
        group => www-data,
    }
}
