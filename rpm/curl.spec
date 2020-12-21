Name:       curl
Summary:    A utility for getting files from remote servers (FTP, HTTP, and others)
Version:    7.74.0
Release:    1
License:    MIT
URL:        https://curl.se/
Source0:    %{name}-%{version}.tar.gz
# patch making libcurl multilib ready
Patch101:   0101-curl-7.32.0-multilib.patch
# use localhost6 instead of ip6-localhost in the curl test-suite
Patch104:   0104-curl-7.73.0-localhost6.patch
# prevent valgrind from reporting false positives on x86_64
Patch105:   0105-curl-7.63.0-lib1560-valgrind.patch

BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libpsl)
BuildRequires:  pkgconfig(libnghttp2)
Provides:   webclient

%description
cURL is a tool for getting files from HTTP, FTP, FILE, LDAP, LDAPS,
DICT, TELNET and TFTP servers, using any of the supported protocols.
cURL is designed to work without user interaction or any kind of
interactivity. cURL offers many useful capabilities, like proxy support,
user authentication, FTP upload, HTTP post, and file transfer resume.

%package -n libcurl
Summary:  A library for getting files from web servers

%description -n libcurl
This package provides a way for applications to use FTP, HTTP, Gopher and
other servers for getting files.

%package -n libcurl-devel
Summary:    Files needed for building applications with libcurl
Requires:   libcurl = %{version}-%{release}
Provides:   curl-devel = %{version}-%{release}
Obsoletes:   curl-devel < %{version}-%{release}

%description -n libcurl-devel
cURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. The libcurl-devel
package includes files needed for developing applications which can
use cURL's capabilities internally.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
%reconfigure --disable-static \
    --enable-ipv6 \
    --enable-symbol-hiding \
    --enable-threaded-resolver \
    --disable-gopher \
    --disable-ldap \
    --disable-ldaps \
    --disable-manual \
    --with-libpsl \
    --with-nghttp2 \
    --without-brotli \
    --without-libidn2 \
    --without-libmetalink \
    --without-libssh

%make_build

%install
%make_install

install -Dp -m 644 docs/libcurl/libcurl.m4 %{buildroot}/%{_datadir}/aclocal/
# don't need curl's copy of the certs; use openssl's
find %{buildroot} -name ca-bundle.crt -exec rm -f '{}' \;

%post -n libcurl -p /sbin/ldconfig

%postun -n libcurl -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_bindir}/curl

%files -n libcurl
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/libcurl.so.*

%files -n libcurl-devel
%defattr(-,root,root,-)
%doc docs/examples/*.c docs/examples/Makefile.example docs/INTERNALS.md
%doc docs/CONTRIBUTE.md docs/libcurl/ABI.md
%{_bindir}/curl-config*
%{_includedir}/curl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%doc %{_mandir}/man1/*
%doc %{_mandir}/man3/*
%{_datadir}/aclocal/libcurl.m4

