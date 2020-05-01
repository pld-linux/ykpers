#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	tests		# unit tests

Summary:	Yubikey personalization program
Summary(pl.UTF-8):	Program do personalizacji urządzeń Yubikey
Name:		ykpers
Version:	1.20.0
Release:	2
License:	BSD
Group:		Applications/System
Source0:	https://developers.yubico.com/yubikey-personalization/Releases/%{name}-%{version}.tar.gz
# Source0-md5:	8749113ce5a0164fe2b429b61242ba0f
Patch0:		%{name}-json-c.patch
URL:		https://developers.yubico.com/yubikey-personalization/
BuildRequires:	asciidoc
BuildRequires:	json-c-devel
BuildRequires:	libusb-devel >=1.0
BuildRequires:	libyubikey-devel >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	udev-devel >= 1:1.188
Requires:	libyubikey >= 1.5
Conflicts:	udev-core < 1:1.188
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Yubico's YubiKey can be re-programmed with a new AES key. This is a
library that makes this an easy task.

%description -l pl.UTF-8
Urządzenia Yubico YubiKey można ponownie zaprogramować nowym kluczem
AES. Ta biblioteka pozwala zrobić to łatwo.

%package devel
Summary:	Development files for ykpers library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki ykpers
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files needed to develop applications
that use ykpers library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe niezbędne do tworzenia aplikacji
wykorzystujących bibliotekę ykpers.

%package static
Summary:	Static ykpers library
Summary(pl.UTF-8):	Statyczna biblioteka ykpers
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ykpers library.

%description static -l pl.UTF-8
Statyczna biblioteka ykpers.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-backend=libusb-1.0 \
	--with-udevrulesdir=/lib/udev/rules.d
%{__make}

%if %{with tests}
export LD_LIBRARY_PATH=$(pwd)/.libs
# disable valgrind, it reports false positives from libc sscanf() and strdup()
%{__make} check \
	LOG_COMPILER=
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libykpers-1.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README doc/Compatibility.asciidoc
%attr(755,root,root) %{_bindir}/ykinfo
%attr(755,root,root) %{_bindir}/ykpersonalize
%attr(755,root,root) %{_bindir}/ykchalresp
%attr(755,root,root) %{_libdir}/libykpers-1.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libykpers-1.so.1
%{_mandir}/man1/ykpersonalize.1*
%{_mandir}/man1/ykchalresp.1*
%{_mandir}/man1/ykinfo.1*
/lib/udev/rules.d/69-yubikey.rules

%files devel
%defattr(644,root,root,755)
%doc doc/USB-Hid-Issue.asciidoc
%attr(755,root,root) %{_libdir}/libykpers-1.so
%{_includedir}/ykpers-1
%{_pkgconfigdir}/ykpers-1.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libykpers-1.a
%endif
