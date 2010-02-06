Summary:        CirrAS management for appliances
Name:           cirras-management
Version:        1.0.0.Beta2
Release:        1
License:        LGPL
Requires:       git
Requires:       shadow-utils
Requires:       ruby
Requires:       initscripts
Requires:       sed
Requires:       sudo
Requires(pre):  rubygems
Requires(pre):  ruby-devel
Requires(pre):  libxml2-devel
Requires(pre):  libxslt-devel
BuildRequires:  ruby
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%description
CirrAS management for appliances.

%install
rm -rf $RPM_BUILD_ROOT

/usr/bin/git clone git://github.com/stormgrind/cirras-management.git $RPM_BUILD_ROOT/usr/share/%{name}

pushd $RPM_BUILD_ROOT/usr/share/%{name}
/usr/bin/git submodule init
/usr/bin/git submodule update
popd

install -d -m 755 $RPM_BUILD_ROOT/var/log/%{name}
install -d -m 755 $RPM_BUILD_ROOT/var/lock
touch $RPM_BUILD_ROOT/var/lock/%{name}.pid

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -r thin 2>/dev/null || :
/usr/sbin/useradd -m -r -g thin thin 2>/dev/null || :

%post
echo "sh /usr/share/%{name}/src/network-setup.sh" >> /etc/rc.local
echo -e "thin ALL = NOPASSWD: ALL\n" >> /etc/sudoers
/bin/sed -i s/"Defaults    requiretty"/"#Defaults    requiretty"/ /etc/sudoers

/usr/bin/gem install -ql /usr/share/%{name}/gems/*.gem &> /usr/share/%{name}/gems/install.log

%files
%defattr(-,root,root)
%attr(644, thin, thin) /var/lock/%{name}.pid
%attr(755, thin, thin) /var/log/%{name}
/

%changelog
* Sat Nov 21 2009 Marek Goldmann 1.0.0.Beta1-1
- Initial release
