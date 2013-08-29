Checkout roswiki repo as (/var/www/wiki.ros.org/)data/plugin.

Apache configuration:

  Alias for custom resources:
    Alias /moin_static197/rostheme/ "/var/www/wiki.ros.org/data/plugin/custom/rostheme/"
    Alias /custom/ "/var/www/wiki.ros.org/data/plugin/custom/"

  Alias for moin resources:
    Alias /moin_static197/ "/var/www/wiki.ros.org/venv/lib/python2.6/site-packages/MoinMoin/web/static/htdocs/"

  Register wsgi:
    WSGIScriptAlias / /var/www/wiki.ros.org/cgi-bin/moin.wsgi
    WSGIDaemonProcess wgmoin user=apache group=apache home=/var/www/wiki.ros.org/data/ processes=50 threads=1 maximum-requests=1000 umask=0007 python-path=/var/www/wiki.ros.org/venv/lib/python2.6/site-packages/
    WSGIProcessGroup wgmoin
