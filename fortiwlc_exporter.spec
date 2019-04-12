%global srcname fortiwlc_exporter
%define version _VERSION_

Name: fortiwlc-exporter
Version: %{version}
Release: 1%{?dist}
Summary: Prometheus exporter for FortiOS WLC
License: MIT
URL: https://git.arnes.si/monitoring/fortiwlc_exporter/
Source0: dist/%{srcname}-%{version}.tar.gz
Source1: %{srcname}.service
Source2: %{srcname}.yaml

%{?systemd_requires}
BuildRequires: systemd
BuildRequires: python34-devel

%description
This project collects data from FortiNET WLC systems and generates export data
for Prometheus.

%prep
%autosetup -n %{srcname}-%{version}

%build
pyinstaller --onefile fortiwlc_exporter/exporter.py -n fortiwlc_exporter

%install
install -p -D -m 755 dist/fortiwlc_exporter %{buildroot}%{_bindir}/fortiwlc_exporter
install -p -D -m 644 %{_sourcedir}/fortiwlc_exporter.service %{buildroot}%{_unitdir}/fortiwlc_exporter.service
install -p -D -m 640 %{_sourcedir}/fortiwlc_exporter.yaml %{buildroot}%{_sysconfdir}/fortiwlc_exporter.yaml

%post
%systemd_post fortiwlc_exporter.service

%preun
%systemd_preun fortiwlc_exporter.service

%postun
%systemd_postun_with_restart fortiwlc_exporter.service

%files
%defattr(-,root,root,-)
%{_bindir}/fortiwlc_exporter
%{_unitdir}/fortiwlc_exporter.service
%config(noreplace) %{_sysconfdir}/fortiwlc_exporter.yaml
