Summary:        Package management framework for Ruby. 
Name:           rubygems
Version:        1.3.5
Release:        1
License:        Ruby License
Requires(pre):  ruby-rdoc
Source0:        http://production.cf.rubygems.org/rubygems/rubygems-%{version}.tgz
Requires:       ruby
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%description
RubyGems is a package management framework for Ruby.

%prep
%setup

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT/usr/share/%{name}
cp -r . $RPM_BUILD_ROOT/usr/share/%{name} 

%post
ruby /usr/share/%{name}/setup.rb 2> /usr/share/%{name}/install.log

%files
%defattr(-,root,root)
/

%changelog
* Sat Nov 21 2009 Marek Goldmann 1.3.5-1
- Initial release
