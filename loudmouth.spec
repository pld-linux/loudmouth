#
# Conditional build:
%bcond_without	apidocs	# disable gtk-doc
%bcond_without	ssl	# without SSL support
#
Summary:	Loudmouth - a Jabber library written in C
Summary(pl.UTF-8):	Loudmouth - biblioteka do obsługi protokołu Jabber napisana w C
Name:		loudmouth
Version:	1.4.3
Release:	4
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/loudmouth/1.4/%{name}-%{version}.tar.bz2
# Source0-md5:	55339ca42494690c3942ee1465a96937
Patch0:		%{name}-async_crash.patch
Patch1:		%{name}-use-gnutls-pc.patch
Patch2:		%{name}-glib.patch
Patch3:		%{name}-link.patch
URL:		https://github.com/mhallendal/loudmouth
# not available (Nov 2013)
#URL:		http://loudmouth.imendio.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.9
BuildRequires:	glib2-devel >= 1:2.12.3
%{?with_ssl:BuildRequires:	gnutls-devel >= 1.4.0}
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.7}
BuildRequires:	libidn-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires:	glib2 >= 1:2.12.3
%{?with_ssl:Requires:	gnutls >= 1.4.0}
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
Requires:	glib2-devel >= 1:2.12.3
%{?with_ssl:Requires:	gnutls-devel >= 1.4.0}

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

%description apidocs
Loudmouth library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Loudmouth.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_ssl:--without-ssl} \
	--with-asyncns \
	--enable-gtk-doc%{!?with_apidocs:=no}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

%{!?with_apidocs:rm -rf $RPM_BUILD_ROOT%{_gtkdocdir}}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libloudmouth-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libloudmouth-1.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libloudmouth-1.so
%{_libdir}/libloudmouth-1.la
%{_pkgconfigdir}/loudmouth-1.0.pc
%{_includedir}/loudmouth-1.0

%files static
%defattr(644,root,root,755)
%{_libdir}/libloudmouth-1.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}
%endif
