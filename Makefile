all:
	# nothing to do

install: all
	install -D -m 0755 check_wordpress.py $(DESTDIR)/usr/lib/mgit-monitoring-plugins/check_wordpress
	install -D -m 0755 check_cached.sh $(DESTDIR)/usr/lib/mgit-monitoring-plugins/check_cached
	install -D -m 0755 check_wordpress_version.php $(DESTDIR)/usr/lib/mgit-monitoring-plugins/check_wordpress_version

deb:
	eatmydata debuild -I -us -uc
