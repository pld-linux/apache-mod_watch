%define		mod_name	watch
%define 	apxs		/usr/sbin/apxs
%include	/usr/lib/rpm/macros.perl
Summary:	Apache module: Monitoring Interface for MRTG
Summary(pl):	Modu� do apache: Interfejs do monitorowania za pomoc� MRTG
Name:		apache-mod_%{mod_name}
Version:	4.03
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	http://www.snert.com/Software/download/mod_watch%(echo %{version} | tr -d .).tgz
# Source0-md5:	06d57713adb935f16596d22256bca913
Source1:	%{name}.conf
URL:		http://www.snert.com/Software/mod_watch/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2
Requires(post,preun):	%{apxs}
Requires(post,preun):	grep
Requires(preun):	fileutils
Requires:	apache >= 2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir	/etc/httpd

%description
This module will watch and collect the bytes, requests, and documents
in & out per virtual host, file owner, remote-ip address, directory or
location, and the web server as a whole. This module was designed for
use with MRTG, which will make nice graphical representations of the
data, but is general enough that it can be applied to other purposes,
as the raw data is accessed by a URL. This module supports
mod_vhost_alias and mod_gzip.

%description -l pl
Ten modu� kontroluje i zbiera informacje na temat ilo�ci przes�anych
bajt�w (przychodz�cych i wychodz�cych) wg. serwera wirtualnego, w�a�ciciela
plik�w, zdalnego adresu ip, katalogu lub lokacji oraz serwera jako ca�o�ci.
Modu� zosta� zaprojektowany do pracy z MRTG, dzi�ki czemu otrzymamy �adn�,
graficzn� reprezentacje danych. Modu� wspiera mod_vhost_alias oraz mod_gzip.

%prep
%setup -q -n mod_%{mod_name}-4.3

%build
%{__make} -f Makefile.dso build \
	APXS=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_bindir},%{_sysconfdir}}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install apache2mrtg.pl mod_watch.pl $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/mod_watch.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f %{_sysconfdir}/httpd.conf ] && \
    ! grep -q "^Include.*mod_watch.conf" %{_sysconfdir}/httpd.conf; then
	echo "Include %{_sysconfdir}/mod_watch.conf" >> %{_sysconfdir}/httpd.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache http daemon."
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	umask 027
	grep -v "^Include.*mod_watch.conf" %{_sysconfdir}/httpd.conf > \
		%{_sysconfdir}/httpd.conf.tmp
	mv -f %{_sysconfdir}/httpd.conf.tmp %{_sysconfdir}/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc CHANGES* *html *.txt Contrib nfields.pl
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_pkglibdir}/*
%{_sysconfdir}/mod_watch.conf
