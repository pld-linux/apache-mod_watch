%define		mod_name	watch
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: Monitoring Interface for MRTG
Summary(pl):	Modu³ do apache: Interfejs do monitorowania za pomoc± MRTG
Name:		apache-mod_%{mod_name}
Version:	3.12
Release:	1
License:	BSD
Group:		Networking/Daemons
Source0:	http://www.snert.com/Software/mod_watch/mod_watch%(echo %{version} | sed -e "s#\.##g").tgz
Source1:	%{name}.conf
URL:		http://www.snert.com/Software/mod_watch/
BuildRequires:	%{apxs}
BuildRequires:	apache(EAPI)-devel
Prereq:		%{_sbindir}/apxs
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define         _sysconfdir     /etc/httpd

%description
This module will watch and collect the bytes, requests, and documents
in & out per virtual host, file owner, remote-ip address, directory or
location, and the web server as a whole. This module was designed for
use with MRTG, which will make nice graphical representations of the
data, but is general enough that it can be applied to other purposes,
as the raw data is accessed by a URL. This module supports
mod_vhost_alias and mod_gzip.

%description -l pl
Ten modu³ kontroluje i zbiera informacje na temat ilo¶ci przes³anych
bajtów (przychodz±cych i wychodz±cych) wg. serwera wirtualnego, w³a¶ciciela
plików, zdalnego adresu ip, katalogu lub lokacji oraz serwera jako ca³o¶ci.
Modu³ zosta³ zaprojektowany do pracy z MRTG, dziêki czemu otrzymamy ³adn±,
graficzn± reprezentacje danych. Modu³ wspiera mod_vhost_alias oraz mod_gzip.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{__make} build-dynamic

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/mod_watch.conf

gzip -9nf CHANGES* apache2mrtg* 

%post
%{_sbindir}/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*mod_watch.conf" /etc/httpd/httpd.conf; then
        echo "Include /etc/httpd/mod_watch.conf" >> /etc/httpd/httpd.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
        grep -v "^Include.*mod_watch.conf" /etc/httpd/httpd.conf > \
                /etc/httpd/httpd.conf.tmp
        mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz *htm
%attr(755,root,root) %{_pkglibdir}/*
