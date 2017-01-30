%bcond_without	tests
Summary:	Yubikey personalization program
Name:		ykpers
Version:	1.18.0
Release:	1
License:	BSD
Group:		Applications/System
URL:		http://opensource.yubico.com/yubikey-personalization/
Source0:	http://opensource.yubico.com/yubikey-personalization/releases/%{name}-%{version}.tar.gz
# Source0-md5:	58e6a7011a3a02ae420a8eee0a442fb1
BuildRequires:	json-c-devel
BuildRequires:	libusb-devel
BuildRequires:	libyubikey-devel
BuildRequires:	systemd-devel

%description
Yubico's YubiKey can be re-programmed with a new AES key. This is a
library that makes this an easy task.

%package devel
Summary:	Development files for ykpers
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header file needed to develop applications
that use ykpers.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	--disable-static \
	--with-udevrulesdir=/lib/udev/rules.d \
	--with-backend=libusb
%{__make}

%if %{with tests}
export LD_LIBRARY_PATH=$RPM_BUILD_DIR/%{name}-%{version}/.libs
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} \
	install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
%{__rm} -rf ${RPM_BUILD_ROOT}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README ChangeLog NEWS
%doc doc/Compatibility.asciidoc
%attr(755,root,root) %{_bindir}/ykinfo
%attr(755,root,root) %{_bindir}/ykpersonalize
%attr(755,root,root) %{_bindir}/ykchalresp
%attr(755,root,root) %ghost %{_libdir}/libykpers-1.so.1
%attr(755,root,root) %{_libdir}/libykpers-1.so.*.*
%{_mandir}/man1/ykpersonalize.1*
%{_mandir}/man1/ykchalresp.1*
%{_mandir}/man1/ykinfo.1*
/lib/udev/rules.d/69-yubikey.rules

%files devel
%defattr(644,root,root,755)
%doc doc/USB-Hid-Issue.asciidoc
%{_pkgconfigdir}/ykpers-1.pc
%attr(755,root,root) %{_libdir}/libykpers-1.so
%{_includedir}/ykpers-1
%{_libdir}/libykpers-1.la
