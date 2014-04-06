Name: gnubatch
Version: 1.10
Release: 1%{?dist}
Summary: gnubatch provides enhanced job control

Group: System Environment/Daemons
License: GPLv3
URL: http://www.gnu.org/software/gnubatch/
Source0: http://ftp.gnu.org/gnu/gnubatch/gnubatch-1.10.tar.gz
Source1: https://github.com/jondkent/gnubatch/blob/master/gnubatch-systemd.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: systemd

%description
gnubatch provides a comprehensive batch scheduling system
for UNIX systems and GNU/Linux with transparently shared jobs and
job control variables across the network.

The first version of the product was written in 1990 and it has been
added to and refined ever since.

This has been edited so as to talk about GNUbatch rather than Xi-Batch
and names suitably changed. It should be able to talk to other
machines running Xi-Batch although the port numbers are different and
will have to be changed on one.


%prep

%setup -a 1

%build
./configure --sysconfdir=/etc/gnubatch --sharedstatedir=/var --localstatedir=/var --exec-prefix=/usr --prefix=/usr
make

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}%{_bindir}
mkdir -p  %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_mandir}/man8/
mkdir -p %{buildroot}%{_mandir}/man3/
mkdir -p %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_mandir}/man5/
mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}
mkdir -p %{buildroot}/usr/share/%{name}/help
mkdir -p %{buildroot}/etc/sysconfig
mkdir -p %{buildroot}/var/gnubatch

cp -p build/.libs/* %{buildroot}/%{_bindir}
cp -p doc/poddoc/man/*.8 %{buildroot}/%{_mandir}/man8/
cp -p doc/poddoc/man/*.3 %{buildroot}/%{_mandir}/man3/
cp -p doc/poddoc/man/*.5 %{buildroot}/%{_mandir}/man5/
cp -p doc/poddoc/man/*.1 %{buildroot}/%{_mandir}/man1/
cp -rp build/lib/.libs/libgnu* %{buildroot}/%{_libdir}
cp -p LICENSE %{buildroot}%{_defaultdocdir}/%{name}/
cp -p README %{buildroot}%{_defaultdocdir}/%{name}/
cp -p build/helpmsg/*help %{buildroot}/usr/share/%{name}/help
cp -p build/helpmsg/btint-config %{buildroot}/usr/share/%{name}/help
cp -p gnubatch.conf %{buildroot}/etc/sysconfig
cp -p lib/systemd/system/gnubatch.service %{buildroot}/%{_unitdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%attr(554,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*
%attr(664,root,root) %{_unitdir}/*
%attr(755,root,root) /var/gnubatch
%attr(666,root,root) /usr/share/%{name}/help/*
%doc LICENSE README
%config(noreplace) %attr(664,root,root) /etc/sysconfig/gnubatch.conf
%{_mandir}/*

%post

echo "checking /etc/services setup for gnubatch"

cat /etc/services | awk '

	$1 ~ /gnubatch/ {\
		if ( $2 == "48104/tcp" ) { print $1 $2; gnubatchtcp = 1; next; }
		}\

	$1 ~ /gnubatch/ {\
		if ( $2 == 48104/udp ) { print $1 $2; gnubatchudp = 1; next; }
		}\

	$1 ~ /gnubatch-feeder/ {\
		if ( $2 == 48105/tcp ) { print $1 $2; gnubatchfeedertcp = 1; next; }
		}\

	$1 ~ /gnubatch-netsrv/ {\
		if ( $2 == 48106/tcp ) { print $1 $2; gnubatchnetsrvtcp = 1; next; }
		}\

	$1 ~ /gnubatch-netsrv/ {\
		if ( $2 == 48106/udp ) { print $1 $2; gnubatchnetsrvudp = 1; next; }
		}\

	$1 ~ /gnubatch-api/ {\
		if ( $2 == 48107/tcp ) { print $1 $2; gnubatchapitcp = 1; next; }
		}\

	$1 ~ /gnubatch-api/ {\
		if ( $2 == 48107/udp ) { print $1 $2; gnubatchapiudp = 1; next; }
		}\

	END {

	if ( ! gnubatchtcp ) { print "gnubatch               48104/tcp        # Connection port"; }
	if ( ! gnubatchudp ) { print "gnubatch               48104/udp        # Connection port"; }
	if ( ! gnubatchfeedertcp ) { print "gnubatch-feeder        48105/tcp        # Feeder port for GNUbatch";}
	if ( ! gnubatchnetsrvtcp ) { print "gnubatch-netsrv        48106/tcp        # External job submission";}
	if ( ! gnubatchnetsrvudp ) { print "gnubatch-netsrv        48106/udp        # Client access";}
	if ( ! gnubatchapitcp ) { print "gnubatch-api           48107/tcp        # API";}
	if ( ! gnubatchapiudp ) { print "gnubatch-api           48107/udp        # API";}
}
' >> /etc/services


%changelog
* Fri Apr 04 2014 Jon Kent <jon.kent at, gmail.com> 1.10-1
- initial fedora release
