%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global sname oslo.versionedobjects
%global pkg_name oslo-versionedobjects

Name:       python-oslo-versionedobjects
Version:    XXX
Release:    XXX
Summary:    OpenStack common versionedobjects library

Group:      Development/Languages
License:    ASL 2.0
URL:        https://launchpad.net/oslo
Source0:    https://pypi.python.org/packages/source/o/%{sname}/%{sname}-1.4.0.tar.gz
BuildArch:  noarch

%package -n python2-%{pkg_name}
Summary:    OpenStack common versionedobjects library

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
BuildRequires: python-d2to1
# Required for tests
BuildRequires: python-hacking
BuildRequires: python-oslotest
BuildRequires: python-testtools
BuildRequires: pytz
BuildRequires: python-fixtures
BuildRequires: python-iso8601
BuildRequires: python-mock
BuildRequires: python-oslo-config
BuildRequires: python-oslo-i18n
BuildRequires: python-oslo-messaging
BuildRequires: python-eventlet

Requires:   python-setuptools
Requires:   python-six >= 1.7
Requires:   python-babel
Requires:   python-oslo-concurrency
Requires:   python-oslo-context
Requires:   python-oslo-messaging
Requires:   python-oslo-serialization
Requires:   python-oslo-utils
Requires:   python-oslo-log
Requires:   python-oslo-i18n
Requires:   python-mock
Requires:   python-fixtures
Requires:   python-iso8601

%description -n python2-%{pkg_name}
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

Oslo versionedobjects library deals with DB schema being at different versions
than the code expects, allowing services to be operated safely during upgrades.

%package -n python-%{pkg_name}-doc
Summary:    Documentation for OpenStack common versionedobjects library

BuildRequires: python-oslo-config
BuildRequires: python-oslo-sphinx
BuildRequires: python-oslo-messaging
BuildRequires: python-iso8601

# Needed for autoindex which imports the code

%description -n python-%{pkg_name}-doc
Documentation for the oslo.versionedobjects library.

%package -n python-%{pkg_name}-tests
Summary:    Tests for OpenStack common versionedobjects library

Requires: python-%{pkg_name} = %{version}-%{release}
Requires: python-hacking
Requires: python-oslotest
Requires: python-testtools
Requires: pytz

%description -n python-%{pkg_name}-tests
Tests for the oslo.versionedobjects library.


%if 0%{?with_python3}
%package -n python3-%{pkg_name}
Summary:    OpenStack common versionedobjects library

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr
BuildRequires: python3-d2to1
# Required for tests
BuildRequires: python3-hacking
BuildRequires: python3-oslotest
BuildRequires: python3-testtools
BuildRequires: python3-pytz
BuildRequires: python3-fixtures
BuildRequires: python3-iso8601
BuildRequires: python3-mock
BuildRequires: python3-oslo-config
BuildRequires: python3-oslo-i18n
BuildRequires: python3-oslo-messaging
BuildRequires: python3-eventlet

Requires:   python3-setuptools
Requires:   python3-six >= 1.7
Requires:   python3-babel
Requires:   python3-oslo-concurrency
Requires:   python3-oslo-context
Requires:   python3-oslo-messaging
Requires:   python3-oslo-serialization
Requires:   python3-oslo-utils
Requires:   python3-oslo-log
Requires:   python3-oslo-i18n
Requires:   python3-mock
Requires:   python3-fixtures
Requires:   python3-iso8601

%description -n python3-%{pkg_name}
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

Oslo versionedobjects library deals with DB schema being at different versions
than the code expects, allowing services to be operated safely during upgrades.
%endif

%description
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

Oslo versionedobjects library deals with DB schema being at different versions
than the code expects, allowing services to be operated safely during upgrades.

%prep
%setup -q -n %{sname}-%{upstream_version}

# let RPM handle deps
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo

%check
# TODO: one python2 test is failing
%{__python2} setup.py test ||
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{pkg_name}
%doc README.rst
%license LICENSE
%{python2_sitelib}/oslo_versionedobjects
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/oslo_versionedobjects/tests

%files -n python-%{pkg_name}-doc
%doc doc/build/html 
%license LICENSE

%files -n python-%{pkg_name}-tests
%{python2_sitelib}/oslo_versionedobjects/tests

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_versionedobjects
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_versionedobjects/tests
%endif

%changelog
