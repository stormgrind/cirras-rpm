#%define jboss_version_full 6.0.0.20100721-M4
%define jboss_version_full 6.0.0-SNAPSHOT

Summary:        JBoss Application Server
Name:           jboss-as6
Version:        6.0.0.SNAPSHOT.20100818.r107578
Release:        1
License:        LGPL
BuildArch:      noarch
Group:          Applications/System
Source0:        http://repo.oddthesis.org/cirras/zip/jboss-as-distribution-6.0.0-SNAPSHOT-20100818-rev-107578.zip
#Source0:        http://internap.dl.sourceforge.net/sourceforge/jboss/jboss-as-distribution-%{jboss_version_full}.zip
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
%setup -n jboss-%{jboss_version_full}

%install
cd %{_topdir}/BUILD

install -d -m 755 $RPM_BUILD_ROOT/opt/%{name}
cp -R jboss-%{jboss_version_full}/* $RPM_BUILD_ROOT/opt/%{name}

# it caused adding bad requires for package
rm -rf $RPM_BUILD_ROOT/opt/%{name}/bin/jboss_init_solaris.sh

install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT/etc/sysconfig

echo "JBOSS_VERSION=%{version}"              > $RPM_BUILD_ROOT/etc/sysconfig/%{name}
echo "JBOSS_HOME=/opt/%{name}"              >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}

chmod 600 $RPM_BUILD_ROOT/etc/sysconfig/%{name} 

%clean
rm -Rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -r %{name} 2>/dev/null || :
/usr/sbin/useradd -c "JBoss AS" -r -s /bin/bash -d /opt/%{name} -g %{name} %{name} 2>/dev/null || :

%post
/sbin/chkconfig --add %{name}

%files
%defattr(-,%{name},%{name})
/

%changelog
* Wed Jul 28 2010 Marek Goldmann 6.0.0.M4-1
- Upgrade to upstream 6.0.0.M4 release 

* Fri May 05 2010 Marek Goldmann 6.0.0.M3-1
- Upgrade to upstream 6.0.0.M3 release

* Wed Feb 17 2010 Marek Goldmann 6.0.0.M2-1
- Upgrade to JBoss AS 6.0.0.M2

* Thu Dec 03 2009 Marek Goldmann 6.0.0.M1-1
- Initial release
