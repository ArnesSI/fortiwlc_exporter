%global srcname fortiwlc_exporter

Name: fortiwlc-exporter
Version: 1.0.0
Release: 1
Summary: FortiWLC Prometheus exporter
License: MIT
URL: https://git.arnes.si/monitoring/fortiwlc_exporter/
Source0: dist/%{srcname}-%{version}.tar.gz
Source1: %{srcname}.service
Source2: %{srcname}.ini
Requires: systemd

BuildRequires: python34-devel
BuildRequires: python34-pip

%description
This project collects data from FortiNET WLC systems and generates export data
for Prometheus.

%prep
%autosetup -n %{srcname}-%{version}
pip3 install pyinstaller
pip3 install .

%build
pyinstaller --onefile fortiwlc_exporter/server.py -n fortiwlc_exporter

%install
install -p -D -m 755 dist/fortiwlc_exporter %{buildroot}%{_bindir}/fortiwlc_exporter
install -p -D -m 644 %{_sourcedir}/fortiwlc_exporter.service %{buildroot}%{_unitdir}/fortiwlc_exporter.service
install -p -D -m 640 %{_sourcedir}/fortiwlc_exporter.ini %{buildroot}%{_sysconfdir}/fortiwlc_exporter.ini

%files
%defattr(-,root,root,-)
%{_bindir}/fortiwlc_exporter
%{_unitdir}/fortiwlc_exporter.service
%config(noreplace) %{_sysconfdir}/fortiwlc_exporter.ini
