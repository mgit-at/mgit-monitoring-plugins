#!/usr/bin/env php5
<?php
// Nagios check for wordpress and plugins version
// Author: Christoph Hack <chack@mgit.at>
// (c) 2016 by mgIT

if($argc != 2) {
	print "usage: check_wordpress_version.php <path to wp installation>\n";
	exit(1);
}

$_SERVER["DOCUMENT_ROOT"] = $argv[1];
chdir($argv[1]);

require_once('./wp-load.php');

global $wp_version;
$core_updates = 0;
$plugin_updates = 0;

wp_version_check();
wp_update_plugins();

$core = get_site_transient('update_core');
$plugins = get_site_transient('update_plugins');

if (isset ($core->updates) && version_compare($core->updates[0]->current, $core->version_checked) > 0) {
	$core_updates = 1;
}

foreach($plugins->response as $plgupd) {
	$plugin_updates = 1;
}

if($core_updates) {
	$text = "core updates available!";
} else {
	$text = "core ok";
}

if($plugin_updates) {
	$text .= "; plugins updates are available!";
} else {
	$text .= "; plugins ok";
}

if($core_updates || $plugin_updates) {
	print("CRITICAL - " . $text."\n");
	exit(2);
} else {
	print("OK - " . $text."\n");
	exit(0);
}

print("CRITICAL - Error in check_wp_versions.php");
exit(2);
?>
