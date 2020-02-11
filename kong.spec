Name:           kong
Version:        2.0.1
Release:        1%{?dist}
Summary:        Kong API Gateway

Group:          Development/System
License:        APL
URL:            https://getkong.org/
Source0:        https://github.com/Kong/kong/archive/%{version}.zip
Source1:        https://openresty.org/download/openresty-1.15.8.2.tar.gz
Source2:        https://github.com/luarocks/luarocks/archive/v3.2.1.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%global debug_package %{nil}
%define rockfile kong-2.0.1-0

%define prefix /usr/local
%define orprefix %{prefix}/openresty
%define luajit %{orprefix}/luajit
%define target /usr/local/kong
%define luarocks %{buildroot}%{luajit}/bin/luajit %{buildroot}%{luajit}/bin/luarocks

%description
This package contains the Kong API Gateway

# ### ### ### ###
# Prep
# ### ### ### ###

%prep
%setup -c -q -n %{name}-%{version} -T -a0 -a1 -a2

# ### ### ### ###
# Build
# ### ### ### ###

%build

# ### ### ### ###
##  pt1 - Executable
# ### ### ### ###

# Build openresty
cd openresty-1.15.8.2
./configure \
  --prefix="%{orprefix}" \
  --with-pcre-jit \
  --with-http_ssl_module \
  --with-http_realip_module \
  --with-http_stub_status_module \
  --with-http_v2_module
make
gmake DESTDIR=%{buildroot} install

cd ../luarocks-3.2.1
./configure \
  --prefix="%{luajit}" \
  --sysconfdir="%{orprefix}/luarocks" \
  --with-lua="%{buildroot}%{luajit}" \
  --with-lua-include="%{buildroot}%{luajit}/include/luajit-2.1" \
  --force-config
make
gmake DESTDIR=%{buildroot} install

# Can't use configure macro here since configure script fails with unsupported
# options

# ### ### ### ###
## pt2 - Documentation
# ### ### ### ###

# Builds HTML documentation
# make luadoc

# ### ### ### ###
# Install
# ### ### ### ###

%install

%{__mkdir} -p %{buildroot}/%{_bindir}
%{__mkdir} -p %{buildroot}/%{target}

%{luarocks} install %{_builddir}/%{name}-%{version}/%{name}-%{version}/%{rockfile}.src.rock --tree %{buildroot}%{target}
for i in %{buildroot}%{target}/bin/*; do
  sed -i 's+%{buildroot}++' $i
done

sed -i 's+%{buildroot}++' %{buildroot}%{luajit}/share/lua/5.1/luarocks/site_config.lua

cd ../kong-%{version}
%{luarocks} pack %{rockfile}.rockspec --tree %{buildroot}%{target}

# ### ### ### ###
# Clean
# ### ### ### ###

%clean
rm -rf %{buildroot}

# ### ### ### ###
# Files
# ### ### ### ###

%files
%{target}
%{orprefix}
%attr(755, %{user}, %{user}) %{target}/kong.lua
# %attr(755, root, root) /etc/init.d/kong
# %config(noreplace) /etc/sysconfig/kong
%attr(755, root, root) %{_bindir}/kong

%changelog
* Thu Feb 6 2020 Black Heat (undefined)
- [WIP] Updated to support Kong 2.0.1.
- [WIP] Added support for Fedora 26+.

* Tue Feb 14 2017 Chris Heald
- Initial packaging