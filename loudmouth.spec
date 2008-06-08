#
# Conditional build:
%bcond_without	apidocs	# disable gtk-doc
%bcond_without	ssl	# without SSL support
#
Summary:	Loudmouth - a Jabber library written in C
Summary(pl.UTF-8):	Loudmouth - biblioteka do obsługi protokołu Jabber napisana w C
Name:		loudmouth
Version:	1.4.0
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/loudmouth/1.4/%{name}-%{version}.tar.bz2
# Source0-md5:	d9504bb4251d4e5b32cb379debda634d
URL:		http://loudmouth.imendio.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel >= 1:2.12.3
%{?with_ssl:BuildRequires:	gnutls-devel >= 1.2.5}
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.7}
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires:	glib2 >= 1:2.12.3
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
%{?with_ssl:Requires:	gnutls-devel >= 1.2.5}

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
Summary(pl.UTF-8):	Dokumentacja API biblioteki Loudmouth.
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Loudmouth library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Loudmouth.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_ssl:--without-ssl} \
	--%{?with_apidocs:en}%{!?with_apidocs:dis}able-gtk-doc
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
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_pkgconfigdir}/*
%{_includedir}/loudmouth-1.0

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}
%endif
