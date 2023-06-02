#
# Conditional build:
%bcond_without	apidocs	# disable gtk-doc
%bcond_without	asyncns	# libasyncns support
%bcond_without	ssl	# SSL support
%bcond_with	openssl	# OpenSSL instead of GnuTLS for SSL

%if %{with ssl} && %{without openssl}
%define	with_gnutls	1
%endif
%if %{without ssl}
%undefine	with_openssl
%endif
Summary:	Loudmouth - a Jabber library written in C
Summary(pl.UTF-8):	Loudmouth - biblioteka do obsługi protokołu Jabber napisana w C
Name:		loudmouth
Version:	1.5.4
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://mcabber.com/files/loudmouth/%{name}-%{version}.tar.bz2
# Source0-md5:	59c9f9f8e6231f38e18876447c608620
Patch0:		%{name}-link.patch
URL:		https://github.com/mcabber/loudmouth/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.9
BuildRequires:	glib2-devel >= 1:2.38.0
%{?with_gnutls:BuildRequires:	gnutls-devel >= 3.0.20}
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.14}
BuildRequires:	heimdal-devel
%{?with_asyncns:BuildRequires:	libasyncns-devel >= 0.3}
BuildRequires:	libidn-devel
BuildRequires:	libtool
%{?with_openssl:BuildRequires:	openssl-devel}
BuildRequires:	pkgconfig
Requires:	glib2 >= 1:2.38.0
%{?with_gnutls:Requires:	gnutls >= 3.0.20}
%{?with_asyncns:Requires:	libasyncns >= 0.3}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Loudmouth is a lightweight and easy-to-use C library for programming
with the Jabber protocol. It's designed to be easy to get started with
and yet extensible to let you do anything the Jabber protocol allows.

%description -l pl.UTF-8
Loudmouth jest lekką i łatwą w obsłudze biblioteką napisaną w języku
C. Służy do obsługi protokołu Jabber. Została zaprojektowana z
naciskiem na prostotę obsługi, pozwala używać wszystkich możliwości
protokołu Jabber.

%package devel
Summary:	Header files and development documentation for Loudmouth library
Summary(pl.UTF-8):	Pliki nagłówkowe Loudmouth, dokumentacja dla programistów
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.38.0
%{?with_asyncns:Requires:	libasyncns-devel >= 0.3}
Requires:	libidn-devel

%description devel
This package provides the necessary header files to allow you to
develop with Loudmouth.

%description devel -l pl.UTF-8
Pakiet zawiera pliki nagłówkowe potrzebne do tworzenia oprogramowania
z wykorzystaniem Loudmouth.

%package static
Summary:	Static libraries for developing with Loudmouth
Summary(pl.UTF-8):	Statyczne biblioteki Loudmouth
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static version of Loudmouth libraries.

%description static -l pl.UTF-8
Statyczna wersja bibliotek Loudmouth.

%package apidocs
Summary:	Loudmouth library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Loudmouth
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
Loudmouth library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Loudmouth.

%prep
%setup -q
%patch0 -p1

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
# default value for with-compile-warnings is "error", which breaks build on glib deprecations
%configure \
	%{?with_asyncns:--with-asyncns} \
	--with-compile-warnings=yes \
	%{!?with_ssl:--without-ssl} \
	%{?with_openssl:--with-ssl=openssl} \
	--enable-gtk-doc%{!?with_apidocs:=no}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libloudmouth-1.la

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_libdir}/libloudmouth-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libloudmouth-1.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libloudmouth-1.so
%{_pkgconfigdir}/loudmouth-1.0.pc
%{_includedir}/loudmouth-1.0

%files static
%defattr(644,root,root,755)
%{_libdir}/libloudmouth-1.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/loudmouth
%endif
