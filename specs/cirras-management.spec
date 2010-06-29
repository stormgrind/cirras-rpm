%define ruby_version 1.8

Summary:        CirrAS management for appliances
Name:           cirras-management
Version:        0.3.0
Release:        1%{?dist}
License:        LGPL
Requires:       shadow-utils
Requires:       ruby
Requires:       initscripts
Requires:       sed
Requires:       sudo
Requires:       initscripts
Requires:       rubygems
BuildRequires:  ruby-devel gcc-c++ rubygems git libxml2-devel libxslt-devel
Requires(post): /sbin/chkconfig
Provides:       /usr/local/bin/ruby
Group:          Development/Tools
Source0:        %{name}.init
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
CirrAS management for appliances.

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE0} $RPM_BUILD_ROOT%{_initrddir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT/usr/lib/ruby/gems/%{ruby_version}

gem install --install-dir=$RPM_BUILD_ROOT/usr/lib/ruby/gems/%{ruby_version} --force --rdoc rack -v 1.2.0
gem install --install-dir=$RPM_BUILD_ROOT/usr/lib/ruby/gems/%{ruby_version} --force --rdoc nokogiri amazon-ec2 sinatra rest-client thin cgi_multipart_eof_fix

/usr/bin/git clone git://github.com/stormgrind/cirras-management.git $RPM_BUILD_ROOT/usr/share/%{name}

install -d -m 755 $RPM_BUILD_ROOT/var/log/%{name}
install -d -m 755 $RPM_BUILD_ROOT/var/lock
touch $RPM_BUILD_ROOT/var/lock/%{name}.pid

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -r thin 2>/dev/null || :
/usr/sbin/useradd -m -r -g thin thin 2>/dev/null || :

%post
/sbin/chkconfig --add %{name}
echo "sh /usr/share/%{name}/src/network-setup.sh" >> /etc/rc.local
echo -e "thin ALL = NOPASSWD: ALL\n" >> /etc/sudoers
/bin/sed -i s/"Defaults    requiretty"/"#Defaults    requiretty"/ /etc/sudoers

%files
%defattr(-,root,root)
%attr(644, thin, thin) /var/lock/%{name}.pid
%attr(755, thin, thin) /var/log/%{name}
/

%changelog
* Sat Nov 21 2009 Marek Goldmann 1.0.0.Beta1-1
- Initial release
