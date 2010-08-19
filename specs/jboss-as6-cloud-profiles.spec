%define jboss_name jboss-as6
%define jboss_version 6.0.0.SNAPSHOT.20100818.r107578
%define jboss_version_full 6.0.0-SNAPSHOT
%define jgroups_version 2.10.0.GA

#%define mod_cluster_version 1.1.0.CR3

Summary:        The JBoss AS 6 cloud profiles (cluster and group)
Name:           jboss-as6-cloud-profiles
Version:        %{jboss_version}
Release:        1
License:        LGPL
BuildArch:      noarch
Group:          Applications/System
Source0:        http://repo.oddthesis.org/cirras/zip/jboss-as-distribution-6.0.0-SNAPSHOT-20100818-rev-107578.zip
#Source0:        http://internap.dl.sourceforge.net/sourceforge/jboss/jboss-as-distribution-%{jboss_version_full}.zip
Source2:        %{jboss_name}-jbossws-host.patch
Source3:        %{jboss_name}-jgroups-s3_ping.patch
Source4:        %{jboss_name}-jvm-route.patch
Source5:        http://heanet.dl.sourceforge.net/sourceforge/javagroups/JGroups-%{jgroups_version}.bin.zip
#Source6:        http://downloads.jboss.org/mod_cluster/%{mod_cluster_version}/mod_cluster-%{mod_cluster_version}-bin.tar.gz
Requires:       %{jboss_name}
BuildRequires:  patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The JBoss AS 6 cloud profiles (cluster and group)

%define __jar_repack %{nil}

%prep
%setup -T -b 0 -n jboss-%{jboss_version_full}
%setup -T -b 5 -n JGroups-%{jgroups_version}.bin
#%setup -T -b 6 -c -n mod_cluster-%{mod_cluster_version}

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

# JGroups update
cp JGroups-%{jgroups_version}.bin/jgroups-%{jgroups_version}.jar $RPM_BUILD_ROOT/opt/%{jboss_name}/server/cluster-ec2/lib/jgroups.jar
cp JGroups-%{jgroups_version}.bin/jgroups-%{jgroups_version}.jar $RPM_BUILD_ROOT/opt/%{jboss_name}/server/cluster/lib/jgroups.jar

# mod_cluster update

#rm -rf $RPM_BUILD_ROOT/opt/%{jboss_name}/server/cluster/deploy/mod_cluster.sar
#rm -rf $RPM_BUILD_ROOT/opt/%{jboss_name}/server/cluster-ec2/deploy/mod_cluster.sar
#rm -rf $RPM_BUILD_ROOT/opt/%{jboss_name}/server/group/deploy/mod_cluster.sar

#cp -r mod_cluster-%{mod_cluster_version}/mod_cluster.sar $RPM_BUILD_ROOT/opt/%{jboss_name}/server/cluster-ec2/deploy/
#cp -r mod_cluster-%{mod_cluster_version}/mod_cluster.sar $RPM_BUILD_ROOT/opt/%{jboss_name}/server/cluster/deploy/
#cp -r mod_cluster-%{mod_cluster_version}/mod_cluster.sar $RPM_BUILD_ROOT/opt/%{jboss_name}/server/group/deploy/

install -d -m 755 $RPM_BUILD_ROOT/etc/sysconfig

echo "JBOSS_CLOUD_DEPLOYMENT=true" > $RPM_BUILD_ROOT/etc/sysconfig/%{name}

cd $RPM_BUILD_ROOT/opt/%{jboss_name}
#patch -p1 < %{SOURCE1}
patch -p1 < %{SOURCE2}
patch -p1 < %{SOURCE3}
patch -p1 < %{SOURCE4}

%clean
rm -Rf $RPM_BUILD_ROOT

%files
%defattr(-,%{jboss_name},%{jboss_name})
/

%changelog
* Wed Jul 28 2010 Marek Goldmann 6.0.0.M4-1
- Upgrade to upstream 6.0.0.M4 release

* Fri May 05 2010 Marek Goldmann 6.0.0.M3-1
- Upgrade to upstream 6.0.0.M3 release

* Wed Feb 17 2010 Marek Goldmann 6.0.0.M2-1
- Upgrade to JBoss AS 6.0.0.M2

* Thu Dec 03 2009 Marek Goldmann 1.0.0.Beta1-1
- Initial release
