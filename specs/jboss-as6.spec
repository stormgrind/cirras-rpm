%define jboss_cache_version 3.2.1.GA

Summary:        JBoss Application Server
Name:           jboss-as6
Version:        6.0.0.M1
Release:        1
License:        LGPL
BuildArch:      noarch
Group:          Applications/System
Source0:        http://internap.dl.sourceforge.net/sourceforge/jboss/jboss-%{version}.zip
Source1:        %{name}.init
Requires:       shadow-utils
Requires:       coreutils
Requires:       java-1.6.0-openjdk
Requires:       initscripts
Requires(post): /sbin/chkconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define runuser %{name}
%define __jar_repack %{nil}

%description
The JBoss Application Server

%prep
%setup -n jboss-%{version}

%install
cd %{_topdir}/BUILD

install -d -m 755 $RPM_BUILD_ROOT/opt/%{name}
cp -R jboss-%{version}/* $RPM_BUILD_ROOT/opt/%{name}

# it caused adding bad requires for package
rm -rf $RPM_BUILD_ROOT/opt/%{name}/bin/jboss_init_solaris.sh

install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}

%clean
rm -Rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -r %{name} 2>/dev/null || :
/usr/sbin/useradd -c "JBoss AS" -r -s /bin/bash -d /opt/%{name} -g %{name} %{name} 2>/dev/null || :

%post
/sbin/chkconfig --add %{name}
/sbin/chkconfig %{name} on

%files
%defattr(-,%{name},%{name})
/

%changelog
* Thu Dec 03 2009 Marek Goldmann 6.0.0.M1-1
- Initial release
