FROM davidva/unibuild-26

MAINTAINER David Va <davidva@tutanota.com>

RUN rm -rf united-build \ 
&& git clone https://github.com/kuboosoft/united-build.git \
&& cd united-build \
&& chmod a+x urpms \
&& ./urpms -g UnitedRPMs/chromium-freeworld -s chromium-freeworld.spec -r true -d 'dist .fc26'

VOLUME ["/var/lib/mock"]
USER root
CMD ["/bin/bash"]



