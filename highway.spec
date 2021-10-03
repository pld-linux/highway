#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	Efficient and performance-portable SIMD
Summary(pl.UTF-8):	Wydajne i przenośne operacje SIMD
Name:		highway
Version:	0.14.2
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/google/highway/releases
Source0:	https://github.com/google/highway/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4821b1064a35baa24ea36994c0d58c41
URL:		https://github.com/google/highway
BuildRequires:	cmake >= 3.10
BuildRequires:	gtest-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Highway is a C++ library for SIMD (Single Instruction, Multiple Data),
i.e. applying the same operation to multiple 'lanes' using a single
CPU instruction.

%description -l pl.UTF-8
Highway to biblioteka C++ do operacji SIMD (Single Instruction,
Multiple Data), czyli wykonywania tej samej operacji na wielu "pasach"
przy użyciu pojedynczej instrukcji procesora.

%package devel
Summary:	Development files for Highway library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki Highway
Group:		Development/Libraries

%description devel
Development files for Highway library.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki Highway.

%package apidocs
Summary:	API documentation for Highway library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Highway
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Highway library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Highway.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DHWY_SYSTEM_GTEST=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc README.md
%{_libdir}/libhwy.a
%{_libdir}/libhwy_contrib.a
%{_includedir}/hwy
%{_pkgconfigdir}/libhwy.pc
%{_pkgconfigdir}/libhwy-contrib.pc
%{_pkgconfigdir}/libhwy-test.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc g3doc/*.{md,pdf}
%endif
