%define jboss_name jboss-as6
%define jboss_version 6.0.0.M2
%define jboss_version_full 6.0.0.20100216-M2

Summary:        The JBoss AS 6 cloud profiles (cluster and group)
Name:           jboss-as6-cloud-profiles
Version:        1.0.0.Beta1
Release:        1
License:        LGPL
BuildArch:      noarch
Group:          Applications/System
Source0:        http://internap.dl.sourceforge.net/sourceforge/jboss/jboss-%{jboss_version}.zip
Source1:        %{jboss_name}-mod_cluster.patch
Source2:        %{jboss_name}-jbossws-host.patch
Source3:        %{jboss_name}-jgroups-s3_ping.patch
Requires:       %{jboss_name}
BuildRequires:  patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The JBoss AS 6 cloud profiles (cluster and group)

%define __jar_repack %{nil}

%prep
%setup -T -b 0 -n jboss-%{jboss_version_full}

%install
rm -Rf $RPM_BUILD_ROOT

cd %{_topdir}/BUILD

# create directories
install -d -m 755 $RPM_BUILD_ROOT/opt/%{jboss_name}/server/cluster-ec2
install -d -m 755 $RPM_BUILD_ROOT/opt/%{jboss_name}/server/cluster
install -d -m 755 $RPM_BUILD_ROOT/opt/%{jboss_name}/server/group

# copy profiles
cp -R jboss-%{jboss_version_full}/server/default/* $RPM_BUILD_ROOT/opt/%{jboss_name}/server/group/
cp -R jboss-%{jboss_version_full}/server/all/* $RPM_BUILD_ROOT/opt/%{jboss_name}/server/cluster/
cp -R jboss-%{jboss_version_full}/server/all/* $RPM_BUILD_ROOT/opt/%{jboss_name}/server/cluster-ec2/

install -d -m 755 $RPM_BUILD_ROOT/etc/sysconfig

echo "JBOSS_CLOUD_DEPLOYMENT=true" > $RPM_BUILD_ROOT/etc/sysconfig/%{name}

cd $RPM_BUILD_ROOT/opt/%{jboss_name}
patch -p1 < %{SOURCE1}
patch -p1 < %{SOURCE2}
patch -p1 < %{SOURCE3}

%clean
rm -Rf $RPM_BUILD_ROOT

%files
%defattr(-,%{jboss_name},%{jboss_name})
/

%changelog
* Wed Feb 17 2010 Marek Goldmann 6.0.0.M2-1
- Upgrade to JBoss AS 6.0.0.M2

* Thu Dec 03 2009 Marek Goldmann 1.0.0.Beta1-1
- Initial release