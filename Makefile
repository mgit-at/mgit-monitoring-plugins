all:
	# nothing to do

install: all
	install -D -m 0755 check_wordpress.py $(DESTDIR)/usr/lib/mgit-monitoring-plugins/check_wordpress

deb:
	eatmydata debuild -I -us -uc
