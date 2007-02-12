# TODO
# - package -DSTATEDIR=/var/lib/mod_watch ?
%define		mod_name	watch
%define 	apxs		/usr/sbin/apxs
%include	/usr/lib/rpm/macros.perl
Summary:	Apache module: Monitoring Interface for MRTG
Summary(pl.UTF-8):   Moduł do apache: Interfejs do monitorowania za pomocą MRTG
Name:		apache-mod_%{mod_name}
Version:	4.03
Release:	5
License:	BSD
Group:		Networking/Daemons
Source0:	http://www.snert.com/Software/download/mod_watch%(echo %{version} | tr -d .).tgz
# Source0-md5:	06d57713adb935f16596d22256bca913
Source1:	%{name}.conf
Patch0:		%{name}-apr-fix.patch
URL:		http://www.snert.com/Software/mod_watch/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.52-2
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This module will watch and collect the bytes, requests, and documents
in & out per virtual host, file owner, remote IP address, directory or
location, and the web server as a whole. This module was designed for
use with MRTG, which will make nice graphical representations of the
data, but is general enough that it can be applied to other purposes,
as the raw data is accessed by a URL. This module supports
mod_vhost_alias and mod_gzip.

%description -l pl.UTF-8
Ten moduł kontroluje i zbiera informacje na temat ilości przesłanych
bajtów (przychodzących i wychodzących) wg. serwera wirtualnego,
właściciela plików, zdalnego adresu IP, katalogu lub lokacji oraz
serwera jako całości. Moduł został zaprojektowany do pracy z MRTG,
dzięki czemu otrzymamy ładną, graficzną reprezentacje danych. Moduł
wspiera mod_vhost_alias oraz mod_gzip.

%prep
%setup -q -n mod_%{mod_name}-4.3
%patch0 -p1

%build
%{__make} -f Makefile.dso build \
	APXS=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_bindir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install apache2mrtg.pl mod_watch.pl $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/99_mod_watch.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc CHANGES* *html *.txt Contrib nfields.pl
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
%attr(755,root,root) %{_bindir}/*
