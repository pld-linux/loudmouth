#
# Conditional build:
%bcond_without ssl	# without SSL support
#
%define		snap	20031128
Summary:	Loudmouth - a Jabber library written in C
Summary(pl):	Loudmouth - biblioteka do obs³ugi protoko³u Jabber napisana w C
Name:		loudmouth
Version:	0.16
Release:	3
License:	LGPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/loudmouth/0.16/%{name}-%{version}.tar.bz2
# Source0-md5:	58bfa1b2ef244c6fd5f69cce7faa4cf5
Patch0:		%{name}-types.patch
Patch1:		%{name}-nolibs.patch
Patch2:		%{name}-gnutls.patch
URL:		http://loudmouth.imendio.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel >= 2.2.0
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	libtool
%{?with_ssl:BuildRequires:	gnutls-devel >= 1.0.9}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Loudmouth is a lightweight and easy-to-use C library for programming
with the Jabber protocol. It's designed to be easy to get started with
and yet extensible to let you do anything the Jabber protocol allows.

%description -l pl
Loudmouth jest lekk± i ³atw± w obs³udze bibliotek± napisan± w jêzyku
C. S³u¿y do obs³ugi protoko³u Jabber. Zosta³a zaprojektowana z
naciskiem na prostotê obs³ugi, pozwala u¿ywaæ wszystkich mo¿liwo¶ci
protoko³u Jabber.

%package devel
Summary:	Header files and development documentation for Loudmouth library
Summary(pl):	Pliki nag³ówkowe Loudmouth, dokumentacja dla programistów
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 2.2.0
Requires:	gtk-doc-common
%{?with_ssl:Requires:	gnutls-devel >= 1.0.6}

%description devel
This package provides the necessary header files to allow you to
develop with Loudmouth.

%description devel -l pl
Pakiet zawiera pliki nag³ówkowe potrzebne do tworzenia oprogramowania
z wykorzystaniem Loudmouth.

%package static
Summary:	Static libraries for developing with Loudmouth
Summary(pl):	Statyczne biblioteki Loudmouth
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static version of Loudmouth libraries.

%description static -l pl
Statyczna wersja bibliotek Loudmouth.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%{?with_ssl:%patch2 -p1}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_ssl:--without-ssl} \
	--enable-gtk-doc

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libloudmouth*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_pkgconfigdir}/*
%{_includedir}/loudmouth-1.0
%{_gtkdocdir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
