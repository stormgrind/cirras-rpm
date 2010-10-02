%define torquebox_version 1.0.0.Beta22

%define jboss_name jboss-as6

Summary:        TorqueBox JRuby
Name:           torquebox-jruby
Version:        %{torquebox_version}
Release:        1
License:        LGPL
BuildArch:      noarch
Group:          Applications/System
Source0:        http://repository.torquebox.org/maven2/releases/org/torquebox/torquebox-dist/1.0.0.Beta22/torquebox-dist-%{torquebox_version}-bin.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The TorqueBox JRuby Distribution

%define __jar_repack %{nil}

%prep
%setup -T -b 0 -n torquebox-%{torquebox_version}

%install
rm -Rf $RPM_BUILD_ROOT

cd %{_topdir}/BUILD

install -d -m 755 $RPM_BUILD_ROOT/opt/

# copy jruby
cp -R torquebox-%{torquebox_version}/jruby $RPM_BUILD_ROOT/opt/

%clean
rm -Rf $RPM_BUILD_ROOT

%files
%defattr(-,%{jboss_name},%{jboss_name})
/

%changelog
* Mon Oct 04 2010 Bob McWhirter 
- Initial release
