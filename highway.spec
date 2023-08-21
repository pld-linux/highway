#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_with	sse2		# SSE2 instructions on x86/x32
%bcond_without	tests		# don't build tests
#
Summary:	Efficient and performance-portable SIMD
Summary(pl.UTF-8):	Wydajne i przenośne operacje SIMD
Name:		highway
Version:	1.0.6
Release:	2
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/google/highway/releases
Source0:	https://github.com/google/highway/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	405abf8d94b618befd44b2cb60a90c0e
Patch0:		%{name}-float16.patch
Patch1:		%{name}-no-avx.patch
URL:		https://github.com/google/highway
BuildRequires:	cmake >= 3.10
%{?with_tests:BuildRequires:	gtest-devel}
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.742
%{?with_sse2:Requires:	cpuinfo(sse2)}
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
Summary:	Header files for Highway library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Highway
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Highway library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Highway.

%package test
Summary:	Highway test helper library
Summary(pl.UTF-8):	Biblioteka pomocnicza testów z użyciem biblioteki Highway
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description test
Highway test helper library.

%description test -l pl.UTF-8
Biblioteka pomocnicza testów z użyciem biblioteki Highway.

%package test-devel
Summary:	Header files for Highway test library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Highway test
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-test = %{version}-%{release}
Requires:	gtest-devel

%description test-devel
Header files for Highway test library.

%description test-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Highway test.

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
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%if %{with sse2}
CXXFLAGS="%{rpmcxxflags} -msse2"
%endif
%cmake .. \
	%{cmake_on_off tests BUILD_TESTING} \
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

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	test -p /sbin/ldconfig
%postun	test -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libhwy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhwy.so.1
%attr(755,root,root) %{_libdir}/libhwy_contrib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhwy_contrib.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhwy.so
%attr(755,root,root) %{_libdir}/libhwy_contrib.so
%dir %{_includedir}/hwy
%{_includedir}/hwy/contrib
%{_includedir}/hwy/ops
%{_includedir}/hwy/*.h
%{_pkgconfigdir}/libhwy.pc
%{_pkgconfigdir}/libhwy-contrib.pc
%{_libdir}/cmake/hwy

%files test
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhwy_test.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhwy_test.so.1

%files test-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhwy_test.so
%{_includedir}/hwy/tests
%{_pkgconfigdir}/libhwy-test.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc g3doc/*.{md,pdf}
%endif
