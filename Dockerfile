FROM blackheat/kong-build-image:fc31-1.5
WORKDIR /root

COPY kong.spec /root/

RUN dos2unix kong.spec
RUN spectool -g -R kong.spec
RUN rpmbuild -ba kong.spec
