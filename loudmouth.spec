Summary:	Loadmouth is a Jabber library written in C.
Summary(pl):	Loadmouth jest bibliotek± do obs³ugi protoko³u Jabber napisan± w C
Name:		loudmouth
Version:	0.9.1
Release:	1
URL:		http://www.imendio.com/projects/loudmouth
Source0:	http://www.imendio.com/projects/loudmouth/src/%{name}-%{version}.tar.gz
License:	LGPL
Group:		Libraries
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:	glib2 >= 2.0.0
Requires(post):	/sbin/ldconfig
BuildRequires:	glib2-devel >= 2.0.0
BuildRequires:	gtk-doc >= 0.10

%description
Loudmouth is a lightweight and easy-to-use C library for programming
with the Jabber protocol. It's designed to be easy to get started with
and yet extensible to let you do anything the Jabber protocol allows.

%description -l pl
Loudmouth jest lekk± i ³atw± w obs³udze bibliotek± napisan± w jêzyku
C. S³u¿y do obs³ugi protoko³u Jabber. Zosta³a zaprojektowana z
naciskiem na prostote obs³ugi, pozwala u¿ywaæ wszystkich mo¿liwo¶ci
protoko³u Jabber.

%package devel
Summary:	Development files for RoadRunner..
Group:		Development/Libraries
Requires:	%name = %{PACKAGE_VERSION}
Requires:	glib2-devel >= 2.0.0
Requires:	gtk-doc-common

%description devel
Loudmouth is a lightweight and easy-to-use C library for programming
with the Jabber protocol. It's designed to be easy to get started with
and yet extensible to let you do anything the Jabber protocol allows.

%description devel -l pl
Loudmouth jest lekk± i ³atw± w obs³udze bibliotek± napisan± w jêzyku
C. S³u¿y do obs³ugi protoko³u Jabber. Zosta³a zaprojektowana z
naciskiem na prostote obs³ugi, pozwala u¿ywaæ wszystkich mo¿liwo¶ci
protoko³u Jabber.


%prep
%setup -q

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-gtk-doc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README COPYING
%{_libdir}/libloudmouth.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_pkgconfigdir}/*
%{_includedir}/loudmouth-1.0
%{_gtkdocdir}/*

%post
/sbin/ldconfig

%postun	-p /sbin/ldconfig
