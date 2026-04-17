#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define 	module	paramiko
Summary:	SSH2 protocol for Python 3
Summary(pl.UTF-8):	Obsługa protokołu SSH2 w Pythonie 3
Name:		python3-%{module}
Version:	4.0.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/paramiko/
Source0:	https://github.com/paramiko/paramiko/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	e5722ec7a749c0449824af27961b62f9
URL:		https://github.com/paramiko/paramiko/
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.9
BuildRequires:	python3-installer
BuildRequires:	python3-setuptools >= 1:77
%if %{with tests}
BuildRequires:	python3-PyNaCl >= 1.5
BuildRequires:	python3-bcrypt >= 3.2
BuildRequires:	python3-cryptography >= 3.3
# optional
#BuildRequires:	python3-gssapi >= 1.4.1
BuildRequires:	python3-invoke >= 2.0
BuildRequires:	python3-pyasn1 >= 0.1.7
BuildRequires:	python3-pytest >= 4.4.2
BuildRequires:	python3-pytest-relaxed >= 2
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-alabaster >= 0.7.13
BuildRequires:	python3-releases >= 2.1
BuildRequires:	sphinx-pdg-3 >= 1.4
%endif
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A module for Python that implements the SSH2 protocol for secure
(encrypted and authenticated) connections to remote machines.

%description -l pl.UTF-8
Moduł dla języka Python implementujący protokół SSH2 w celu uzyskania
bezpiecznych (szyfrowanych i autoryzowanych) połączeń ze zdalnymi
maszynami.

%package apidocs
Summary:	API documentation for paramiko module
Summary(pl.UTF-8):	Dokumentacja API modułu paramiko
Group:		Documentation

%description apidocs
API documentation for paramiko module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu paramiko.

%prep
%setup -q -n %{module}-%{version}

# Windows-specific modules, break tests by using Windows-specific ctypes API
%{__rm} paramiko/{win_pageant,_winapi}.py

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests -m 'not slow'
%endif

%if %{with doc}
sphinx-build-3 -b html sites/docs sites/docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a demos/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
%{__sed} -i -e '1s,/usr/bin/env python$,%{__python3},' $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}/*.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst SECURITY.md TODO sites/www/changelog.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info
%{_examplesdir}/python3-%{module}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc sites/docs/_build/html/{_static,api,*.html,*.js}
%endif
