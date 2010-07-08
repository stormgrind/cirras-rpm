%define agent_name rhq-enterprise-agent

Summary:        RHQ Agent
Name:           rhq-agent
Version:        3.0.0
Release:        1
License:        LGPL
BuildArch:      noarch
Source0:        http://downloads.sourceforge.net/project/rhq/rhq/rhq-%{version}/rhq-server-%{version}.zip
Source1:        rhq-agent.init
Source2:        rhq-agent-install.sh
Group:          Applications/System
Requires:       java-1.6.0-openjdk
Requires(post): /sbin/chkconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Probably this is not a good idea, but this is the only way to create a noarch package
# This package contains several libraries, I only found glibc requires, add other here too 
AutoReqProv:    no
Requires:       glibc

%define runuser %{name}
%define __jar_repack %{nil}

%description
The RHQ project is an abstraction and plug-in based systems management suite that provides extensible and integrated systems management for multiple products and platforms across a set of core features. The project is designed with layered modules that provide a flexible architecture for deployment. It delivers a core user interface that delivers audited and historical management across an entire enterprise. A Server/Agent architecture provides remote management and plugins implement all specific support for managed products. RHQ is an open source project licensed under the GPL, with some pieces individually licensed under a dual GPL/LGPL license to facilitate the integration with extended packages such as Jopr and Embedded Jopr.

%prep
rm -rf $RPM_BUILD_DIR
unzip -q %{SOURCE0} rhq-server-%{version}/jbossas/server/default/deploy/rhq.ear.rej/rhq-downloads/rhq-agent/rhq-enterprise-agent-%{version}.jar -d $RPM_BUILD_DIR
cd $RPM_BUILD_DIR/rhq-server-%{version}/jbossas/server/default/deploy/rhq.ear.rej/rhq-downloads/rhq-agent/ && jar xf rhq-enterprise-agent-%{version}.jar
unzip -q $RPM_BUILD_DIR/rhq-server-%{version}/jbossas/server/default/deploy/rhq.ear.rej/rhq-downloads/rhq-agent/rhq-enterprise-agent-%{version}.zip

%build

%install
install -d -m 755 $RPM_BUILD_ROOT/opt/%{name}-%{version}

cp -R $RPM_BUILD_DIR/rhq-server-%{version}/jbossas/server/default/deploy/rhq.ear.rej/rhq-downloads/rhq-agent/rhq-agent/* $RPM_BUILD_ROOT/opt/%{name}-%{version}

install -d -m 755 $RPM_BUILD_ROOT/etc/sysconfig

echo "RHQ_AGENT_VERSION=%{version}"              > $RPM_BUILD_ROOT/etc/sysconfig/%{name}
echo "RHQ_AGENT_HOME=/opt/%{name}-%{version}"   >> $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT/usr/share/%{name}
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/%{name}/rhq-agent-install.sh

%clean
rm -Rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -r %{name} 2>/dev/null || :
/usr/sbin/useradd -c "%{name}" -r -s /bin/bash -d /opt/%{name}-%{version} -g %{name} %{name} 2>/dev/null || :

%post
/sbin/chkconfig --add %{name}
/sbin/chkconfig %{name} on

%files
%defattr(-,root,root)
/

%changelog
* Thu Jul 08 2010 Marek Goldmann 3.0.0
- Upgrade to upstream 3.0.0 release

* Tue Jun 29 2010 Marek Goldmann 3.0.0.B06
- Upgrade to upstream 3.0.0.B06 release

* Fri May 05 2010 Marek Goldmann 3.0.0.B05
- Upgrade to upstream 3.0.0.B05 release

* Mon Feb 22 2010 Marek Goldmann 3.0.0.B03
- Upgrade to upstream 3.0.0.B03 release

* Mon Feb 01 2010 Marek Goldmann 3.0.0.B01
- Upgrade to upstream 3.0.0.B01 release

* Tue Dec 24 2009 Marek Goldmann 1.4.0.B01
- Upgrade to version 1.4.0.B01

* Thu Sep 24 2009 Marek Goldmann 1.3.1
- Upgrade to version 1.3.1

* Sat Jul 25 2009 Marek Goldmann 1.2.1
- Initial packaging
