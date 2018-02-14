Name:       curl
Summary:    A utility for getting files from remote servers (FTP, HTTP, and others)
Version:    7.58.0
Release:    1
Group:      Applications/Internet
License:    MIT
URL:        http://curl.haxx.se/
Source0:    %{name}-%{version}.tar.gz
Patch2:     0101-curl-7.32.0-multilib.patch
Patch5:     0104-curl-7.19.7-localhost6.patch
Patch6:     0106-curl-7.36.0-libssh2-valgrind.patch
Patch7:     0107-curl-7.21.4-libidn-valgrind.patch

BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  libtool
Provides:   webclient


%description
cURL is a tool for getting files from HTTP, FTP, FILE, LDAP, LDAPS,
DICT, TELNET and TFTP servers, using any of the supported protocols.
cURL is designed to work without user interaction or any kind of
interactivity. cURL offers many useful capabilities, like proxy support,
user authentication, FTP upload, HTTP post, and file transfer resume.



%package -n libcurl
Summary:    A library for getting files from web servers
Group:      System/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libcurl
This package provides a way for applications to use FTP, HTTP, Gopher and
other servers for getting files.


%package -n libcurl-devel
Summary:    Files needed for building applications with libcurl
Group:      Development/Libraries
Requires:   libcurl = %{version}-%{release}
Requires:   libidn-devel
Provides:   curl-devel = %{version}-%{release}
Obsoletes:   curl-devel < %{version}-%{release}

%description -n libcurl-devel
cURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. The libcurl-devel
package includes files needed for developing applications which can
use cURL's capabilities internally.



%prep
%setup -q -n %{name}-%{version}/%{name}

%patch2 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
./buildconf
%configure --disable-static \
    --enable-ipv6 \
    --disable-gopher

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

install -d $RPM_BUILD_ROOT/%{_datadir}/aclocal
install -m 644 docs/libcurl/libcurl.m4 $RPM_BUILD_ROOT/%{_datadir}/aclocal
# don't need curl's copy of the certs; use openssl's
find ${RPM_BUILD_ROOT} -name ca-bundle.crt -exec rm -f '{}' \;








%post -n libcurl -p /sbin/ldconfig

%postun -n libcurl -p /sbin/ldconfig




%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/curl

%files -n libcurl
%defattr(-,root,root,-)
%{_libdir}/libcurl.so.*

%files -n libcurl-devel
%defattr(-,root,root,-)
%doc docs/examples/*.c docs/examples/Makefile.example docs/INTERNALS.md
%doc docs/CONTRIBUTE.md docs/libcurl/ABI
%{_bindir}/curl-config*
%{_includedir}/curl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%doc %{_mandir}/man1/*
%doc %{_mandir}/man3/*
%{_datadir}/aclocal/libcurl.m4

