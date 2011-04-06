%define drupaldir %{_datadir}/drupal7
Name: drupal7
Version:  7.0
Release:  4%{?dist}
Summary: An open-source content-management platform

Group: Applications/Publishing
License: GPLv2+ and BSD
URL: http://www.drupal.org
Source0: http://ftp.osuosl.org/pub/drupal/files/projects/drupal-%{version}.tar.gz
Source1: %{name}.conf
Source2: %{name}-README.fedora
Source3: %{name}-cron
Source4: %{name}-files-migrator.sh
Patch0:  %{name}-7.0-scripts-noshebang.patch

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: php, php-gd, php-mbstring, wget, php-pdo, php-xml

%description
Equipped with a powerful blend of features, Drupal is a Content Management 
System written in PHP that can support a variety of websites ranging from
personal weblogs to large community-driven websites.  Drupal is highly
configurable, skinnable, and secure.

%prep

%setup -q -n drupal-%{version}

%patch0 -p0

chmod -x scripts/drupal.sh
chmod -x scripts/password-hash.sh
chmod -x scripts/run-tests.sh

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{drupaldir}
cp -pr * %{buildroot}%{drupaldir}
cp -pr .htaccess %{buildroot}%{drupaldir}
mkdir -p %{buildroot}%{_sysconfdir}/httpd
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
cp -pr %SOURCE1 %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/modules
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/themes
mv %{buildroot}%{drupaldir}/sites/* %{buildroot}%{_sysconfdir}/%{name}
rmdir %{buildroot}%{drupaldir}/sites
ln -s ../../..%{_sysconfdir}/%{name} %{buildroot}%{drupaldir}/sites
mkdir -p %{buildroot}%{_docdir}
cp -pr %SOURCE2 .
install -D -p -m 0644 %SOURCE3 %{buildroot}%{_sysconfdir}/cron.hourly/%{name}
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/files/default
ln -s ../../..%{_localstatedir}/lib/%{name}/files/default %{buildroot}%{_sysconfdir}/%{name}/default/files
cp -pr %SOURCE4 .
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
mv %{buildroot}%{drupaldir}/.htaccess %{buildroot}%{_sysconfdir}/httpd/conf.d/drupal7-site.htaccess
ln -s ../../../%{_sysconfdir}/httpd/conf.d/drupal7-site.htaccess %{buildroot}%{drupaldir}/.htaccess
mv %{buildroot}%{_sysconfdir}/%{name}/example.sites.php .

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.txt INSTALL* LICENSE* MAINTAINERS.txt UPGRADE.txt %{name}-README.fedora sites/all/README.txt %{name}-files-migrator.sh
%doc COPYRIGHT.txt README.txt example.sites.php
%{drupaldir}
%exclude %{drupaldir}/CHANGELOG.txt
%exclude %{drupaldir}/INSTALL* 
%exclude %{drupaldir}/LICENSE* 
%exclude %{drupaldir}/MAINTAINERS.txt 
%exclude %{drupaldir}/UPGRADE.txt
%exclude %{drupaldir}/COPYRIGHT.txt
%exclude %{drupaldir}/README.txt
%dir %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/%{name}/all
%exclude %{_sysconfdir}/%{name}/all/README.txt
%config(noreplace) %{_sysconfdir}/%{name}/default
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}*.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}*.htaccess
%attr(755,root,apache) %config(noreplace) %{_sysconfdir}/cron.hourly/%{name}
%dir %attr(775,root,apache) %{_localstatedir}/lib/%{name}/
%dir %attr(775,root,apache) %{_localstatedir}/lib/%{name}/files/
%dir %attr(775,root,apache) %{_localstatedir}/lib/%{name}/files/default/

%changelog
* Wed Apr 06 2011 Jon Ciesla <limb@jcomserv.net> - 7.0-4
- Exlcuded README and COPYRIGHT.
- Fixed sites symlink.

* Tue Mar 29 2011 Jon Ciesla <limb@jcomserv.net> - 7.0-3
- Fixed sites symlink.
- Moved example.sites.php to doc.
- Fixed year in changelog.
- Added php-pdo and php-xml requires.
- Corrected license tag.

* Fri Feb 25 2011 Jon Ciesla <limb@jcomserv.net> - 7.0-2
- Corrected license tag.

* Wed Jan 05 2011 Jon Ciesla <limb@jcomserv.net> - 7.0-1
- Initial packaging.
