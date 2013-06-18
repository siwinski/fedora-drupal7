# Disable automatic requires/provides processing
AutoReqProv: no

%define drupaldir %{_datadir}/drupal7
Name: drupal7
Version:  7.22
Release:  6%{?dist}
Summary: An open-source content-management platform

Group: Applications/Publishing
License: GPLv2+ and BSD and MIT
URL: http://www.drupal.org
Source0: http://ftp.osuosl.org/pub/drupal/files/projects/drupal-%{version}.tar.gz
Source1: %{name}.conf
Source2: %{name}-README.fedora
Source3: %{name}-cron
Source4: %{name}-files-migrator.sh
Source5: macros.%{name}
Source6: %{name}.attr
Source7: %{name}.prov
Source8: macros.%{name}.rpm-lt-4-9-compat
Source9: %{name}.prov.rpm-lt-4-9-compat
Source10: %{name}.req
Source11: %{name}.req.rpm-lt-4-9-compat
Patch0:  %{name}-7.4-scripts-noshebang.patch
Patch1:  drupal-7.14-CVE-2012-2922.patch

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: php, php-gd, php-mbstring, wget, php-pdo, php-xml

# Virtual provides
## Core
Provides: drupal7(core) = %{version}
## Modules
Provides: drupal7(aggregator) = %{version}
Provides: drupal7(block) = %{version}
Provides: drupal7(blog) = %{version}
Provides: drupal7(book) = %{version}
Provides: drupal7(color) = %{version}
Provides: drupal7(comment) = %{version}
Provides: drupal7(contact) = %{version}
Provides: drupal7(contextual) = %{version}
Provides: drupal7(dashboard) = %{version}
Provides: drupal7(dblog) = %{version}
Provides: drupal7(field_sql_storage) = %{version}
Provides: drupal7(field_ui) = %{version}
Provides: drupal7(field) = %{version}
Provides: drupal7(file) = %{version}
Provides: drupal7(filter) = %{version}
Provides: drupal7(forum) = %{version}
Provides: drupal7(help) = %{version}
Provides: drupal7(image) = %{version}
Provides: drupal7(list) = %{version}
Provides: drupal7(locale) = %{version}
Provides: drupal7(menu) = %{version}
Provides: drupal7(node) = %{version}
Provides: drupal7(number) = %{version}
Provides: drupal7(openid) = %{version}
Provides: drupal7(options) = %{version}
Provides: drupal7(overlay) = %{version}
Provides: drupal7(path) = %{version}
Provides: drupal7(php) = %{version}
Provides: drupal7(poll) = %{version}
Provides: drupal7(rdf) = %{version}
Provides: drupal7(search) = %{version}
Provides: drupal7(shortcut) = %{version}
Provides: drupal7(simpletest) = %{version}
Provides: drupal7(statistics) = %{version}
Provides: drupal7(syslog) = %{version}
Provides: drupal7(system) = %{version}
Provides: drupal7(taxonomy) = %{version}
Provides: drupal7(text) = %{version}
Provides: drupal7(toolbar) = %{version}
Provides: drupal7(tracker) = %{version}
Provides: drupal7(translation) = %{version}
Provides: drupal7(trigger) = %{version}
Provides: drupal7(update) = %{version}
Provides: drupal7(user) = %{version}
## Themes
Provides: drupal7(bartik) = %{version}
Provides: drupal7(garland) = %{version}
Provides: drupal7(seven) = %{version}
Provides: drupal7(stark) = %{version}emes
## Profiles
Provides: drupal7(minimal) = %{version}
Provides: drupal7(standard) = %{version}

%description
Equipped with a powerful blend of features, Drupal is a Content Management
System written in PHP that can support a variety of websites ranging from
personal weblogs to large community-driven websites.  Drupal is highly
configurable, skinnable, and secure.

%package rpmbuild
Summary: Rpmbuild files for %{name}
Group:   Development/Tools

%description rpmbuild
%{summary}.

%prep
%setup -q -n drupal-%{version}

%patch0 -p1
%patch1 -p0

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
mv %{buildroot}%{drupaldir}/sites/* %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/all/libraries
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

# rpmbuild
# RPM >= 4.9
%if 0%{?_fileattrsdir:1}
mkdir -p %{buildroot}%{_sysconfdir}/rpm/
install -pm0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/rpm/macros.%{name}
mkdir -p %{buildroot}%{_prefix}/lib/rpm/fileattrs
install -pm0644 %{SOURCE6} %{buildroot}%{_prefix}/lib/rpm/fileattrs/%{name}.attr
install -pm0755 %{SOURCE7} %{buildroot}%{_prefix}/lib/rpm/%{name}.prov
install -pm0755 %{SOURCE10} %{buildroot}%{_prefix}/lib/rpm/%{name}.req
# RPM < 4.9
%else
mkdir -p %{buildroot}%{_sysconfdir}/rpm/
install -pm0644 %{SOURCE8} %{buildroot}%{_sysconfdir}/rpm/macros.%{name}
mkdir -p %{buildroot}%{_prefix}/lib/rpm/
install -pm0755 %{SOURCE9} %{buildroot}%{_prefix}/lib/rpm/%{name}.prov
install -pm0755 %{SOURCE11} %{buildroot}%{_prefix}/lib/rpm/%{name}.req
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.txt INSTALL* LICENSE* MAINTAINERS.txt UPGRADE.txt %{name}-README.fedora sites/README.txt %{name}-files-migrator.sh
%doc COPYRIGHT.txt README.txt example.sites.php
%{drupaldir}
%exclude %{drupaldir}/CHANGELOG.txt
%exclude %{drupaldir}/INSTALL*
%exclude %{drupaldir}/LICENSE*
%exclude %{drupaldir}/MAINTAINERS.txt
%exclude %{drupaldir}/UPGRADE.txt
%exclude %{drupaldir}/COPYRIGHT.txt
%exclude %{drupaldir}/README.txt
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/rpm/macros.drupal7
%config(noreplace) %{_sysconfdir}/%{name}/all
%exclude %{_sysconfdir}/%{name}/README.txt
%config(noreplace) %{_sysconfdir}/%{name}/default
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}*.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}*.htaccess
%attr(755,root,apache) %config(noreplace) %{_sysconfdir}/cron.hourly/%{name}
%dir %attr(775,root,apache) %{_localstatedir}/lib/%{name}/
%dir %attr(775,root,apache) %{_localstatedir}/lib/%{name}/files/
%dir %attr(775,root,apache) %{_localstatedir}/lib/%{name}/files/default/

%files rpmbuild
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.drupal7
%{?_fileattrsdir:%{_prefix}/lib/rpm/fileattrs/%{name}.attr}
%{_prefix}/lib/rpm/%{name}.prov
%{_prefix}/lib/rpm/%{name}.req

%changelog
* Tue Jun 18 2013 Jon Ciesla <limburgher@gmail.com> - 7.22-6
- Add AllowOverride All to drupal7.conf, BZ 905912.

* Mon Jun 03 2013 Jon Ciesla <limburgher@gmail.com> - 7.22-5
- Add auto-requires, BZ 969593.

* Tue May 21 2013 Jon Ciesla <limburgher@gmail.com> - 7.22-4
- Allow use of auto-provides <= EL-6.

* Thu May 09 2013 Jon Ciesla <limburgher@gmail.com> - 7.22-3
- Change rpmconfigdir to %%{_prefix}/lib/rpm to support EL-5.

* Thu May 09 2013 Jon Ciesla <limburgher@gmail.com> - 7.22-2
- Add libraries directory and macro, BZ 959687.
- Add auto-provides, BZ 959683.

* Thu Apr 4 2013 Peter Borsa <peter.borsa@gmail.com> - 7.22-1
- 7.22

* Thu Mar 7 2013 Peter Borsa <peter.borsa@gmail.com> - 7.21-1
- 7.21

* Thu Feb 21 2013 Paul W. Frields <stickster@gmail.com> - 7.20-1
- 7.20, SA-CORE-2013-002 (#913403)

* Fri Jan 25 2013 Jon Ciesla <limburgher@gmail.com> - 7.19-2
- README update for cron_key, BZ 902234.

* Thu Jan 17 2013 Jon Ciesla <limburgher@gmail.com> - 7.19-1
- 7.19, SA-CORE-2013-001.

* Thu Dec 20 2012 Jon Ciesla <limburgher@gmail.com> - 7.18-1
- 7.18.

* Thu Nov 8 2012 Peter Borsa <peter.borsa@gmail.com> - 7.17-2
- Fix README.txt location.

* Thu Nov 8 2012 Peter Borsa <peter.borsa@gmail.com> - 7.17-1
- New upstream.

* Wed Oct 31 2012 Jon Ciesla <limburgher@gmail.com> - 7.16-3
- Fix conf.

* Tue Oct 30 2012 Jon Ciesla <limburgher@gmail.com> - 7.16-2
- Fix for httpd 2.4, BZ 871394.

* Wed Oct 17 2012 Orion Poplawski <orion@cora.nwra.com> - 7.16-1
- New upstream - SA-CORE-2012-003 security update

* Wed Aug 1 2012 Peter Borsa <peter.borsa@gmail.com> - 7.15-1
- New upstream.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Jon Ciesla <limburgher@gmail.com> - 7.14-2
- Patch for CVE-2012-2922, BZ 824631, BZ 824632.

* Thu May  3 2012 Paul W. Frields <stickster@gmail.com> - 7.14-1
- New upstream. (#818538)

* Thu Feb 02 2012 Jon Ciesla <limburgher@gmail.com> - 7.12-1
- New upstream.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Jon Ciesla <limburgher@gmail.com> - 7.10-1
- New upstream, BZ 760504.

* Thu Oct 27 2011 Paul W. Frields <stickster@gmail.com> - 7.9-1
- New upstream, BZ 749509.

* Sat Sep  3 2011 Paul W. Frields <stickster@gmail.com> - 7.8-1
- New upstream, minor bugfixes and API improvements only.

* Sun Aug  7 2011 Paul W. Frields <stickster@gmail.com> - 7.7-1
- New upstream, fixed version string only.

* Wed Jul 27 2011 Jon Ciesla <limb@jcomserv.net> - 7.6-1
- New upstream, SA-CORE-2011-003, BZ 726243.

* Thu Jun 30 2011 Jon Ciesla <limb@jcomserv.net> - 7.4-1
- New upstream, SA-CORE-2011-002, BZ 717874.
- Dropped unused dirs in /etc/drupal7/, BZ 703736.

* Fri Jun 17 2011 Jon Ciesla <limb@jcomserv.net> - 7.2-2
- Bump and rebuild for BZ 712251.

* Thu May 26 2011 Jon Ciesla <limb@jcomserv.net> - 7.2-1
- New upstream, SA-CORE-2011-001.

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
