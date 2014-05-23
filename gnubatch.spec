Name: gnubatch
Version: 1.10
Release: 7%{?dist}
Summary: Distributed job scheduler with job dependancy support

License: GPLv3+
URL: http://www.gnu.org/software/gnubatch/
Source0: http://ftp.gnu.org/gnu/gnubatch/gnubatch-%{version}.tar.gz
Source1: https://github.com/jondkent/gnubatch/blob/master/gnubatch.service

BuildRequires: systemd ncurses-devel libtool bison flex-devel
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
GNUbatch is a job scheduler to run under Unix and GNU/Linux operating systems. It executes jobs at specified dates and times or according to dependencies or interlocks defined by the user.

Schedules of jobs may be run on just one processor, or shared across several processors on a network with network-wide dependencies. Access to jobs and other facilities may be restricted to one user or several users in a group as required.

Jobs can be chained together, with optional paths based on errors, and these chains can be created to span multiple machines. For example, you could have a reporting task that runs on a collection of machines, which then causes a single job to run on another machine to aggregate the results into a report.

%prep

%setup -q

%build
%configure
sed -i 's!\(.*gcc_useful_options.*\)"$!\1 \${RPM_OPT_FLAGS}"!' config.status ; ./config.status
make RPM_OPT_FLAGS="%{optflags}"


%install

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_mandir}/man8/
mkdir -p %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_mandir}/man5/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}/help
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_localstatedir}/gnubatch

install -pm 755 build/.libs/* %{buildroot}%{_bindir}
install -pm 644 doc/poddoc/man/*.8 %{buildroot}%{_mandir}/man8/
install -pm 644 doc/poddoc/man/*.5 %{buildroot}%{_mandir}/man5/
install -pm 644 doc/poddoc/man/*.1 %{buildroot}%{_mandir}/man1/
install -pm 755 build/lib/.libs/libgnu* %{buildroot}%{_libdir}
install -pm 644 build/helpmsg/*help %{buildroot}%{_datadir}/%{name}/help
install -pm 644 build/helpmsg/btint-config %{buildroot}%{_datadir}/%{name}/help
install -pm 644 gnubatch.conf %{buildroot}%{_sysconfdir}/sysconfig
install -pm 644 %{SOURCE1} %{buildroot}%{_unitdir}

%post

cat %{_sysconfdir}/services | awk '

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
' >> %{_sysconfdir}/services

/sbin/ldconfig
%systemd_post gnubatch.service

%preun
%systemd_preun gnubatch.service

%postun
%systemd_postun_with_restart gnubatch.service
/sbin/ldconfig

%files
%{_bindir}/*
%{_libdir}/*
%{_unitdir}/*
%dir %{_localstatedir}/gnubatch
%{_datadir}/%{name}/
%doc LICENSE README
%config(noreplace) %{_sysconfdir}/sysconfig/gnubatch.conf
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
* Fri May 23 2014 Jon Kent <jon.kent at, gmail.com> 1.10-7
- replace /var and /etc with relevant macro - bugzilla 1084813
- added missing systemd post/preun/postun Requires - bugzilla 1084813

* Tue May 13 2014 Jon Kent <jon.kent at, gmail.com> 1.10-6
- tidy up of %files to remove redundant entries - bugzilla 1084813

* Sat May 10 2014 Jon Kent <jon.kent at, gmail.com> 1.10-5
- added sed post configure editing and modifed make statement (with thanks to Michael Schwendt) - bugzilla 1084813

* Fri Apr 18 2014 Jon Kent <jon.kent at, gmail.com> 1.10-4
- additional spec file changes as per package review feedback - bugzilla 1084813

* Wed Apr 16 2014 Jon Kent <jon.kent at, gmail.com> 1.10-3
- spec file changes as per package review feedback - bugzilla 1084813

* Sat Apr 12 2014 Jon Kent <jon.kent at, gmail.com> 1.10-2
- added buildrequires for ncurses-devel, libtool, bison, flex and flex-devel

* Fri Apr 04 2014 Jon Kent <jon.kent at, gmail.com> 1.10-1
- initial fedora release

