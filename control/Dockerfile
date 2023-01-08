# Use the container that comes with `cross` as a base. It's already got
# a cross-compile toolchain installed, so that's less work for us.
FROM rustembedded/cross:armv7-unknown-linux-gnueabihf-0.2.1

RUN apt-get update
RUN dpkg --add-architecture armhf && \
    apt-get update && \
    apt-get install --assume-yes apt-utils libssl-dev:armhf libasound2-dev:armhf libudev-dev:armhf

# New!
ENV PKG_CONFIG_LIBDIR_armv7_unknown_linux_gnueabihf=/usr/lib/arm-linux-gnueabihf/pkgconfig
ENV PKG_CONFIG_PATH=/usr/lib/arm-linux-gnueabihf/pkgconfig