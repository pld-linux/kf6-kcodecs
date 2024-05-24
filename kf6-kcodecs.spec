#
# Conditional build:
%bcond_with	tests		# build with tests
# TODO:
# - runtime Requires if any
%define		kdeframever	6.2
%define		qtver		5.15.2
%define		kfname		kcodecs

Summary:	String encoding
Name:		kf6-%{kfname}
Version:	6.2.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	5d6c21ce5f50a614930f5044da249a82
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	gperf
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6Core >= %{qtver}
Requires:	kf6-dirs
Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KCodecs provide a collection of methods to manipulate strings using
various encodings. It supports:

- base64
- uu
- quoted-printable

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Core-devel >= %{qtver}
Requires:	cmake >= 3.16
Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF6Codecs.so.6
%attr(755,root,root) %{_libdir}/libKF6Codecs.so.*.*
%{_datadir}/qlogging-categories6/kcodecs.categories
%{_datadir}/qlogging-categories6/kcodecs.renamecategories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF6Codecs.so
%{_includedir}/KF6/KCodecs
%{_libdir}/cmake/KF6Codecs
