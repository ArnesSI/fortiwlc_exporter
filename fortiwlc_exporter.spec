%global srcname fortiwlc_exporter
%define version _VERSION_

Name: fortiwlc-exporter
Version: %{version}
Release: 1%{?dist}
Summary: Prometheus exporter for FortiOS WLC
License: MIT
URL: https://git.arnes.si/monitoring/%{srcname}/
Source0: dist/%{srcname}-%{version}.tar.gz
Source1: %{srcname}.service
Source2: %{srcname}.yaml

Requires(pre): shadow-utils
%{?systemd_requires}
BuildRequires: systemd
BuildRequires: python34-devel

%description
This project collects data from FortiNET WLC systems and generates export data
for Prometheus.

%prep
%autosetup -n %{srcname}-%{version}

%build
pyinstaller --onefile %{srcname}/exporter.py -n %{srcname}

%install
install -p -D -m 755 dist/%{srcname} %{buildroot}%{_bindir}/%{srcname}
install -p -D -m 644 %{_sourcedir}/%{srcname}.service %{buildroot}%{_unitdir}/%{srcname}.service
install -p -D -m 640 %{_sourcedir}/%{srcname}.yaml %{buildroot}%{_sysconfdir}/%{srcname}.yaml

%pre
getent group %{srcname} >/dev/null || groupadd -r %{srcname}
getent passwd %{srcname} >/dev/null || \
    useradd -r -g %{srcname} -d / -s /sbin/nologin \
    -c "%{srcname} systemd user" %{srcname}
exit 0

%post
%systemd_post %{srcname}.service

%preun
%systemd_preun %{srcname}.service

%postun
%systemd_postun_with_restart %{srcname}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{srcname}
%{_unitdir}/%{srcname}.service
%config(noreplace) %{_sysconfdir}/%{srcname}.yaml
