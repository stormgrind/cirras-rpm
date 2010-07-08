%define rhq_name rhq-cli

Summary:        RHQ Helper for CirrAS
Name:           cirras-rhq
Version:        3.0.0
Release:        1
License:        LGPL
BuildArch:      noarch
Source0:        rhq-cli-install.sh
Source1:        import-servers.js
Source2:        import-servers.sh
Group:          Applications/System
Requires:       java-1.6.0-openjdk
Requires:       unzip
Requires:       cronie
Requires:       initscripts
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Helps with importing and configuring RHQ in CirrAS environment.

%install
install -d -m 755 $RPM_BUILD_ROOT/etc/sysconfig

echo "RHQ_CLI_VERSION=%{version}"    > $RPM_BUILD_ROOT/etc/sysconfig/%{rhq_name}
echo "RHQ_CLI_HOME=/opt/%{rhq_name}-%{version}"    >> $RPM_BUILD_ROOT/etc/sysconfig/%{rhq_name}
echo "RHQ_CLI_USERNAME=rhqadmin"        >> $RPM_BUILD_ROOT/etc/sysconfig/%{rhq_name}
echo "RHQ_CLI_PASSWORD=rhqadmin"        >> $RPM_BUILD_ROOT/etc/sysconfig/%{rhq_name}
echo "RHQ_SERVER_PORT=7080"             >> $RPM_BUILD_ROOT/etc/sysconfig/%{rhq_name}

install -d -m 755 $RPM_BUILD_ROOT/usr/share/%{name}
install -d -m 755 $RPM_BUILD_ROOT/var/log/%{name}
install -m 744 %{SOURCE0} $RPM_BUILD_ROOT/usr/share/%{name}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/usr/share/%{name}
install -m 744 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/%{name}

%clean
rm -Rf $RPM_BUILD_ROOT

%post
echo "sh /usr/share/%{name}/rhq-cli-install.sh &" >> /etc/rc.local
echo '* * * * * /usr/share/%{name}/import-servers.sh >> /var/log/%{name}/import.log' | crontab -

%files
%defattr(-,root,root)
/

%changelog
* Thu Jul 08 2010 Marek Goldmann 3.0.0
- Upgrade to upstream 3.0.0 release

* Fri May 05 2010 Marek Goldmann 3.0.0.B05
- Upgrade to upstream 3.0.0.B05 release

* Thu Feb 23 2010 Marek Goldmann 1.0.0.Beta2
- Version upgrade

* Thu Jan 28 2010 Marek Goldmann 1.0.0.Beta1
- Initial packaging
