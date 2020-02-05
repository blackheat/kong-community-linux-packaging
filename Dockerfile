FROM blackheat/kong-build-image:fc31-1.4
WORKDIR /root

COPY kong.spec /root/

RUN spectool -g -R kong.spec
RUN rpmbuild -ba kong.spec
