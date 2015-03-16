%global sname oslo.versionedobjects

Name:       python-oslo-versionedobjects
Version:    XXX
Release:    XXX{?dist}
Summary:    OpenStack common versionedobjects library

Group:      Development/Languages
License:    ASL 2.0
URL:        https://launchpad.net/oslo
Source0:    https://pypi.python.org/packages/source/o/%{sname}/%{sname}-1.4.0.tar.gz

BuildArch:  noarch
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

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr
BuildRequires: python-d2to1

%description
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

Oslo versionedobjects library deals with DB schema being at different versions
than the code expects, allowing services to be operated safely during upgrades.

%package doc
Summary:    Documentation for OpenStack common versionedobjects library
Group:      Documentation

BuildRequires: python-oslo-sphinx

# Needed for autoindex which imports the code

%description doc
Documentation for the oslo.versionedobjects library.

%prep
%setup -q -n %{sname}-%{upstream_version}

# let RPM handle deps
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
sphinx-build -b html -d build/doctrees   source build/html
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo

%check

%files
%doc README.rst LICENSE
%{python_sitelib}/oslo_versionedobjects
%{python_sitelib}/*.egg-info

%files doc
%doc doc/build/html LICENSE

%changelog
* Mon Mar 16 2015 Derek Higgins <derekh@redhat.com> - XXX
- Initial package.
