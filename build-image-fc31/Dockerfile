FROM fedora:31
RUN dnf update -y
RUN dnf groupinstall -y "Development Tools"
RUN dnf install -y rpm-build spectool pcre pcre-devel openssl openssl-devel zlib-devel
RUN mkdir -p /root/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}