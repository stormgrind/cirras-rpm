%define torquebox_version 1.0.0.Beta22

%define jboss_name jboss-as6

Summary:        TorqueBox Cloud Profile Deployers
Name:           torquebox-cloud-profile-deployers
Version:        %{torquebox_version}
Release:        1
License:        LGPL
BuildArch:      noarch
Group:          Applications/System
Source0:        http://repository.torquebox.org/maven2/releases/org/torquebox/torquebox-dist/1.0.0.Beta22/torquebox-dist-%{torquebox_version}-bin.zip
Requires:       %{jboss_name}-cloud-profiles
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The TorqueBox Cloud Profiles Deployers

%define __jar_repack %{nil}

%prep
%setup -T -b 0 -n torquebox-%{torquebox_version}

%install
rm -Rf $RPM_BUILD_ROOT

cd %{_topdir}/BUILD

install -d -m 755 $RPM_BUILD_ROOT/opt/%{jboss_name}/server/cluster-ec2/deployers
install -d -m 755 $RPM_BUILD_ROOT/opt/%{jboss_name}/server/cluster/deployers
install -d -m 755 $RPM_BUILD_ROOT/opt/%{jboss_name}/server/group/deployers


# copy profiles
cp -R torquebox-%{torquebox_version}/jboss/server/all/deployers/torquebox.deployer/ $RPM_BUILD_ROOT/opt/%{jboss_name}/server/cluster-ec2/deployers/
cp -R torquebox-%{torquebox_version}/jboss/server/all/deployers/torquebox.deployer/ $RPM_BUILD_ROOT/opt/%{jboss_name}/server/cluster/deployers/
cp -R torquebox-%{torquebox_version}/jboss/server/all/deployers/torquebox.deployer/ $RPM_BUILD_ROOT/opt/%{jboss_name}/server/group/deployers/

%clean
rm -Rf $RPM_BUILD_ROOT

%files
%defattr(-,%{jboss_name},%{jboss_name})
/

%changelog
* Mon Oct 04 2010 Bob McWhirter 
- Initial release
