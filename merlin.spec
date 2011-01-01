Name:		merlin
Version:	0.9.0
Release:	%mkrel 1
Summary:	Nagios distributed monitoring
License:	BSD
Group:		Networking/Other
URL:		www.op5.org/community/plugin-inventory/op5-projects/merlin
Source:     http://op5.org/op5media/op5.org/downloads/merlin-%{version}.tar.gz
BuildRequires: dbi-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
The Merlin project, or Module for Effortless Redundancy and Loadbalancing In
Nagios, was initially started to create an easy way to set up distributed
Nagios installations, allowing Nagios processes to exchange information
directly as an alternative to the standard nagios way using NSCA. When starting
the Ninja project we realised that we could continue the work on Merlin and
adopt the project to function as backend for Ninja by adding support for
storing the status information in a database, fault tolearance and some other
cool things. This means that Merlin now are responsible for providing status
data, acting as a backend, for the Ninja GUI.

%prep
%setup -q

%build
%make

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_libdir}/merlin
install -m 755 import showlog merlind %{buildroot}%{_libdir}/merlin
install -m 644 merlin.so import.php object_importer.inc.php %{buildroot}%{_libdir}/merlin

install -d -m 755 %{buildroot}%{_sysconfdir}
install -m 644 example.conf %{buildroot}%{_sysconfdir}/merlin.conf
perl -pi \
    -e 's|@\@DESTDIR@\@/logs|%{_localstatedir}/log/merlin|;' \
    -e 's|@\@DESTDIR@\@/ipc.sock|%{_localstatedir}/lib/merlin/ipc.sock|;' \
    %{buildroot}%{_sysconfdir}/merlin.conf

install -d -m 755 %{buildroot}%{_localstatedir}/log/merlin
install -d -m 755 %{buildroot}%{_localstatedir}/lib/merlin

install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 init.sh %{buildroot}%{_initrddir}/merlind
perl -pi \
    -e 's|^BINDIR=.*|BINDIR=%{_libdir}/merlin|;' \
    -e 's|^CONFIG_FILE=.*|CONFIG_FILE=%{_sysconfdir}/merlin.conf|;' \
    %{buildroot}%{_initrddir}/merlind

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc TECHNICAL SPECS README HOWTO COPYING
%{_initrddir}/merlind
%{_libdir}/merlin
%{_localstatedir}/lib/merlin
%{_localstatedir}/log/merlin
%config(noreplace)%{_sysconfdir}/merlin.conf

