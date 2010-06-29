%define mod_cluster_arch x86
%define mod_cluster_bit 32

%ifarch x86_64
	%define mod_cluster_arch x64
	%define mod_cluster_bit 64
%endif

Summary:    JBoss mod_cluster for Apache httpd
Name:       mod_cluster
Version:    1.1.0.CR3
Release:    1
License:    LGPL
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Group:      Applications/System
Requires:   httpd-devel >= 2.2.8
Source:     http://downloads.jboss.org/mod_cluster/%{version}/mod_cluster-%{version}-linux2-%{mod_cluster_arch}-so.tar.gz
Source2:    mod_cluster.conf

%description
JBoss mod_cluster for Apache httpd

%prep
rm -rf %{name}-%{mod_cluster_bit}
%setup -T -b 0 -c -n %{name}-%{mod_cluster_bit}

%install

cd %{_topdir}/BUILD

%define httpd_modules_dir /usr/lib/httpd/modules

%ifarch x86_64
	%define httpd_modules_dir /usr/lib64/httpd/modules
%endif

modules=( mod_advertise mod_manager mod_proxy_cluster mod_slotmem )

# mod_proxy_ajp mod_proxy_http

pushd %{name}-%{mod_cluster_bit}

install -d -m 755 $RPM_BUILD_ROOT%{httpd_modules_dir}

for module in ${modules[@]} ; do
  cp ${module}.so $RPM_BUILD_ROOT%{httpd_modules_dir}
done

popd

install -d -m 755 $RPM_BUILD_ROOT/etc/httpd/conf.d
cp %{SOURCE2} $RPM_BUILD_ROOT/etc/httpd/conf.d/

install -d -m 755 $RPM_BUILD_ROOT/usr/share/%{name}
echo "%{version}" > $RPM_BUILD_ROOT/usr/share/%{name}/VERSION

%clean
rm -Rf $RPM_BUILD_ROOT

%pre

%post

pushd /etc/httpd/conf > /dev/null

cp httpd.conf httpd.conf.orig
sed s/"^LoadModule proxy_balancer_module"/"#LoadModule proxy_balancer_module"/ httpd.conf.orig > httpd.conf

popd > /dev/null

%preun

pushd /etc/httpd/conf > /dev/null

rm -f httpd.conf.orig > /dev/null
cp httpd.conf httpd.conf.orig
sed s/"^#LoadModule proxy_balancer_module"/"LoadModule proxy_balancer_module"/ httpd.conf.orig > httpd.conf

popd > /dev/null

%files
%defattr(-,root,root)
/

%changelog
* Tue Jun 29 2010 Marek Goldmann 1.0.0.CR3
- Upgrade to upstream 1.0.0.CR3 release

* Fri May 05 2010 Marek Goldmann 1.0.0.CR1
- Upgrade to upstream 1.0.0.CR1

* Thu Dec 03 2009 Marek Goldmann 1.1.0.Beta1
- Update to 1.1.0.Beta1

* Sat May 30 2009 Marek Goldmann 1.0.0.GA
- Update to 1.0.0.GA

* Tue Apr 28 2009 Marek Goldmann 1.0.0.CR1
- Using compiled modules

* Thu Mar 26 2009 Marek Goldmann 1.0.0.CR1
- Update to 1.0.0.CR1

* Fri Feb 20 2009 Marek Goldmann 1.0.0.Beta4
- Update to 1.0.0.Beta4

* Wed Feb 04 2009 Marek Goldmann 1.0.0.Beta3
- Commenting proxy_balancer_module

* Tue Dec 30 2008 Marek Goldmann 1.0.0.Beta2
- Added support for x86_64 arch

* Mon Dec 29 2008 Mob McWhirter 1.0.0.Beta2
- Initial packaging for Fedora 10 i386

