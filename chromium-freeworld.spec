#
# spec file for package chromium-freeworld
#
# Copyright (c) 2020 UnitedRPMs.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://goo.gl/zqFJft
#

# These spec file includes some tips and patches thanks to:
#  [1] https://www.archlinux.org/packages/extra/x86_64/chromium/
#  [2] https://packages.gentoo.org/packages/www-client/chromium
#  [3] https://build.opensuse.org/package/show/openSUSE:Factory/chromium
#  [4] https://pkgs.fedoraproject.org/cgit/rpms/chromium.git 
#  [5] http://copr-dist-git.fedorainfracloud.org/cgit/lantw44/chromium/chromium.git
#  [6] https://salsa.debian.org/chromium-team/chromium/tree/master/debian
#  [7] http://www.linuxfromscratch.org/blfs/view/cvs/xsoft/chromium.html
#  [8] https://aur.archlinux.org/packages/chromium-gtk2/
#  [9] https://github.com/RussianFedora/chromium/
#  [10] http://svnweb.mageia.org/packages/cauldron/chromium-browser-stable/?pathrev=1321923
#  [11] https://gitlab.com/noencoding/OS-X-Chromium-with-proprietary-codecs/wikis/List-of-all-gn-arguments-for-Chromium-build
#  [12] https://operasoftware.github.io/upstreamtools/
#  [13] https://build.opensuse.org/package/show/network:chromium/chromium-beta
#  [14] https://github.com/saiarcot895/chromium-ubuntu-build
#  [15] https://git.exherbo.org/desktop.git/tree/packages/net-www/chromium-stable

%undefine _debuginfo_subpackages
%undefine _debugsource_packages

# Turn off the brp-python-bytecompile automagic
%global _python_bytecompile_extra 0

%global chromiumdir %{_libdir}/chromium
%global crd_path %{_libdir}/chrome-remote-desktop
# Do not check any ffmpeg or libmedia bundle files in libdir for requires
%global __requires_exclude_from ^%{chromiumdir}/libffmpeg.*$
%global __requires_exclude_from ^%{chromiumdir}/libmedia.*$

# Generally chromium is a monster if you compile the source code, enabling all; and takes hours compiling; common users doesn't need all tools.
%bcond_with devel_tools
# Chromium users doesn't need chrome-remote-desktop
%bcond_with remote_desktop
#
# Get the version number of latest stable version
# $ curl -s 'https://omahaproxy.appspot.com/all?os=linux&channel=stable' | sed 1d | cut -d , -f 3
%bcond_with normalsource

# clang is necessary for a fast build
%bcond_without clang
# 

# About clang bundle: Necessary in cases where "clang" in system, fails to build chromium.
%if 0%{?fedora} <= 32
%bcond_without clang_bundle
%else
%bcond_with clang_bundle
%endif

# jinja conditional
%bcond_with system_jinja2


# markupsafe
%bcond_with system_markupsafe


# https://github.com/dabeaz/ply/issues/66
%bcond_with system_ply

# Require libxml2 > 2.9.4 for XML_PARSE_NOXXE
%bcond_without system_libxml2

# Require harfbuzz >= 1.5.0 for hb_glyph_info_t
# hb-aat.h isn't in system anymore...
%bcond_with system_harfbuzz

# Allow testing whether icu can be unbundled
%bcond_with system_libicu

# Allow disabling unconditional build dependency on clang
%bcond_without require_clang

# In UnitedRPMs, we have openh264
%bcond_without system_openh264

# Now is easy to use the external ffmpeg...
%bcond_without system_ffmpeg

# Jumbo / Unity builds (deprecated)
# https://chromium.googlesource.com/chromium/src/+/lkcr/docs/jumbo.md
%bcond_with jumbo_unity

# Vaapi conditional
%bcond_without vaapi

# Gtk2 conditional
%bcond_with gtk2

# re2 conditional
%bcond_with re2_external

# swiftshader conditional
%bcond_with swiftshader

# 
%define _legacy_common_support 1

Name:       chromium-freeworld
Version:    86.0.4240.111
Release:    13.1
Summary:    An open-source project that aims to build a safer, faster, and more stable browser

Group:      Applications/Internet
License:    BSD and LGPLv2+
URL:        https://www.chromium.org
Vendor:     URPMS

%if %{with normalsource}
Source0:    https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
%endif
Source1:    chromium-latest.py
Source2:    BUILD.gn
# https://bugs.freedesktop.org/show_bug.cgi?id=106490
Source3:    %{name}-drirc-disable-10bpc-color-configs.conf
%if %{with remote_desktop}
Source33:   chrome-remote-desktop.service
%endif

# The following two source files are copied and modified from
# https://repos.fedorapeople.org/repos/spot/chromium/
Source10:   chromium-wrapper.txt
Source11:   chromium-freeworld.desktop

# The following two source files are copied verbatim from
# http://pkgs.fedoraproject.org/cgit/rpms/chromium.git/tree/
Source12:   chromium-freeworld.xml
Source13:   chromium-freeworld.appdata.xml

# Unpackaged fonts
Source14:	https://github.com/UnitedRPMs/chromium-freeworld/releases/download/fonts/Garuda.ttf
Source15:	https://fontlibrary.org/assets/downloads/gelasio/4d610887ff4d445cbc639aae7828d139/gelasio.zip
Source16:	http://download.savannah.nongnu.org/releases/freebangfont/MuktiNarrow-0.94.tar.bz2
Source17:	https://chromium.googlesource.com/chromium/src.git/+archive/refs/heads/master/third_party/test_fonts.tar.gz
Source18:	https://github.com/web-platform-tests/wpt/raw/master/fonts/Ahem.ttf
Source19:	https://chromium.googlesource.com/chromium/src/+archive/66.0.3359.158/third_party/gardiner_mod.tar.gz
Source20:	https://github.com/UnitedRPMs/chromium-freeworld/releases/download/fonts/arimo.tar.xz
Source21:	https://github.com/UnitedRPMs/chromium-freeworld/releases/download/fonts/cousine.tar.xz
# markupsafe
Source22:	https://github.com/pallets/markupsafe/archive/1.1.1.tar.gz
# Clang bundle
%if %{with clang_bundle}
Source23:	https://github.com/llvm/llvm-project/releases/download/llvmorg-11.0.0/clang+llvm-11.0.0-x86_64-linux-gnu-ubuntu-20.04.tar.xz
%endif
# V8 missed/test 
#Source24:	https://github.com/v8/v8/archive/7.5.48.tar.gz
Source25:	https://github.com/UnitedRPMs/chromium-freeworld/releases/download/gn/gn-linux-amd64.zip


#----------------------------------------------------------------------------------------------------------------------------
# Patches 
Patch0: only-fall-back-to-the-i965-driver-if-we-re-on-iHD.patch
Patch1: check-for-enable-accelerated-video-decode-on-Linux.patch
Patch2: widevine-allow-on-linux.patch
Patch3: chromium-nacl-llvm-ar.patch
Patch4: chromium-python2.patch
Patch5: chromium-79-gcc-protobuf-alignas.patch
Patch6: chromium-80-QuicStreamSendBuffer-deleted-move-constructor.patch
Patch7: chromium-84-blink-disable-clang-format.patch
Patch8: chromium-fix-char_traits.patch
Patch9: chromium-86-nearby-explicit.patch
Patch10: chromium-86-nearby-include.patch
Patch11: chromium-86-compiler.patch
Patch13: chromium-86-ServiceWorkerRunningInfo-noexcept.patch
Patch14: chromium-86-ConsumeDurationNumber-constexpr.patch
Patch15: chromium-86-ImageMemoryBarrierData-init.patch
Patch16: chromium-remove-new-lld-flags.patch
Patch17: chromium-gl_defines_fix.patch

# VAAPI
Patch12: enable-vaapi-on-linux.diff
#

Patch22: gtk2.patch



ExclusiveArch: x86_64 

%if %{with clang} || %{with require_clang} 
BuildRequires: clang llvm
%endif
# Basic tools and libraries
BuildRequires: ninja-build 
BuildRequires: bison 
BuildRequires: gperf 
BuildRequires: hwdata 
BuildRequires: gn 
BuildRequires: java-1.8.0-openjdk
BuildRequires: xz
BuildRequires: unzip
#BuildRequires: glibc32
BuildRequires: libgcc(x86-32) 
BuildRequires: glibc(x86-32) 
BuildRequires: redhat-rpm-config
BuildRequires: libatomic
BuildRequires: libcap-devel 
BuildRequires: cups-devel 
BuildRequires: alsa-lib-devel
%if 0%{?fedora} >= 30
BuildRequires:	minizip-compat-devel
%else
BuildRequires:	minizip-devel
%endif
BuildRequires: pkgconfig(libexif) 
BuildRequires: pkgconfig(nss) 
%if %{with gtk2}
BuildRequires: pkgconfig(gtk+-2.0)
%else
BuildRequires: pkgconfig(gtk+-3.0)
%endif
BuildRequires: python2-devel
%if 0%{?fedora} >= 29
BuildRequires:	python-unversioned-command
%endif
BuildRequires: pkgconfig(xtst) 
BuildRequires: pkgconfig(xscrnsaver)
BuildRequires: pkgconfig(dbus-1) 
BuildRequires: pkgconfig(libudev)
#BuildRequires: pkgconfig(gnome-keyring-1)
BuildRequires: pkgconfig(libffi)
# remove_bundled_libraries.py --do-remove
BuildRequires: python2-rpm-macros
#BuildRequires: python-beautifulsoup4
#BuildRequires: python-html5lib

%if %{with system_markupsafe}
%if 0%{?fedora} >= 26
BuildRequires: python2-markupsafe
%else
BuildRequires: python-markupsafe
%endif
%endif

%if %{with system_ply}
BuildRequires: python2-ply
%endif
# replace_gn_files.py --system-libraries
BuildRequires: flac-devel
%if %{with system_harfbuzz}
BuildRequires: harfbuzz-devel
%endif
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng-devel
# Chromium requires libvpx 1.5.0 and some non-default options
BuildRequires: libvpx-devel
BuildRequires: libwebp-devel
BuildRequires: pkgconfig(libxslt)
BuildRequires: opus-devel
%if %{with system_libxml2}
BuildRequires: pkgconfig(libxml-2.0)
%endif
%if %{with re2_external}
BuildRequires: re2-devel
%endif
%if %{with system_openh264}
BuildRequires: openh264-devel
%endif
BuildRequires: snappy-devel
BuildRequires: yasm
BuildRequires: zlib-devel
# use_*
BuildRequires: pciutils-devel
BuildRequires: speech-dispatcher-devel
BuildRequires: pulseaudio-libs-devel
# Only for non-normal source
BuildRequires: wget
# install desktop files
BuildRequires: desktop-file-utils
# install AppData files
BuildRequires: libappstream-glib
# remote desktop needs this
BuildRequires: pam-devel
BuildRequires: systemd
# CLANG
%if %{with clang}
BuildRequires: clang
%endif 
# markupsafe missed
BuildRequires: git
BuildRequires: nodejs
BuildRequires: libdrm-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libEGL-devel
# vulcan
#BuildRequires: vulkan-devel
%if %{with system_libicu}
BuildRequires: libicu-devel
%endif
# ffmpeg external conditional
%if %{with system_ffmpeg}
BuildRequires: ffmpeg-devel >= 4.3
%endif
%if %{with vaapi}
BuildRequires:	libva-devel 
%endif
BuildRequires:  pkgconfig(libtcmalloc)
#unbundle fontconfig avoid fails in start
BuildRequires:	fontconfig-devel 
# fonts
BuildRequires:	google-croscore-arimo-fonts
BuildRequires:	google-croscore-cousine-fonts
BuildRequires:	dejavu-sans-fonts
BuildRequires:	thai-scalable-garuda-fonts
BuildRequires:	lohit-devanagari-fonts
BuildRequires:	lohit-gurmukhi-fonts
BuildRequires:	lohit-tamil-fonts
BuildRequires:	google-noto-sans-cjk-jp-fonts
BuildRequires:	google-noto-sans-khmer-fonts
BuildRequires:	google-croscore-tinos-fonts
BuildRequires:	subversion
BuildRequires:	at-spi2-core-devel
%if %{with clang_bundle}
BuildRequires:	ncurses-compat-libs
BuildRequires:  z3-libs
%endif
BuildRequires:	libevent-devel
BuildRequires:  expat-devel
BuildRequires:  mesa-libgbm-devel

%if 0%{?fedora} >= 32
BuildRequires:	pipewire0.2-devel
%else
BuildRequires:	pipewire-devel >= 0.2
%endif

BuildRequires:	python2-jinja2
	
# gn needs these
BuildRequires:  libstdc++-static
BuildRequires:	libstdc++-devel, openssl-devel

BuildRequires:  nasm

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires: hicolor-icon-theme
%if %{with re2_external}
Requires: re2
%endif
Requires: %{name}-libs = %{version}-%{release}

%if %{with vaapi}
Requires: libva-vdpau-driver
Requires: libva-intel-driver
Requires: libva-intel-hybrid-driver 
%endif

%if 0%{?fedora}
# This enables support for u2f tokens
Recommends: u2f-hidraw-policy
%endif

Obsoletes: chromium = %{version}-%{release}
Recommends: liberation-fonts
Recommends: chromium-pepper-flash
Recommends: chromium-widevine

%description
Chromium is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

This is the stable channel Chromium browser. It offers a rock solid
browser which is updated with features and fixes once they have been
thoroughly tested. If you want the latest features, install the
chromium-unstable package instead.

Note: If you are reverting from unstable to stable or beta channel, you may
experience tab crashes on startup. This crash only affects tabs restored
during the first launch due to a change in how tab state is stored.
See http://bugs.chromium.org/34688. It's always a good idea to back up
your profile before changing channels.

%package libs
Summary: Shared libraries used by chromium (and chrome-remote-desktop)
%if !%{with system_ffmpeg}
Requires: %{name}-libs-media%{_isa} = %{version}-%{release}
%endif
Provides: %{name}-libs%{_isa} = %{version}-%{release}
Obsoletes: chromium-libs = %{version}-%{release}

%description libs
Shared libraries used by chromium (and chrome-remote-desktop).

%if %{with devel_tools}
%package chromedriver
Summary: WebDriver for Google Chrome/Chromium
Group: Development/Libraries
Provides: chromedriver >= 54

%description chromedriver
WebDriver is an open source tool for automated testing of webapps across many
browsers. It provides capabilities for navigating to web pages, user input,
JavaScript execution, and more. ChromeDriver is a standalone server which
implements WebDriver's wire protocol for Chromium. It is being developed by
members of the Chromium and WebDriver teams.
%endif

%if !%{with system_ffmpeg}
%package libs-media
Summary: Chromium media libraries built with all possible codecs
Provides: %{name}-libs-media%{_isa} = %{version}-%{release}
Provides: libffmpeg.so()(64bit) 

%description libs-media
Chromium media libraries built with all possible codecs. Chromium is an
open-source web browser, powered by WebKit (Blink). This package replaces
the default chromium-libs-media package, which is limited in what it
can include.
%endif

%if %{with remote_desktop}
%package -n chrome-remote-desktop
Summary: Remote desktop support for google-chrome & chromium
Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: xorg-x11-server-Xvfb

Requires: %{name}-libs%{_isa} = %{version}-%{release}

%description -n chrome-remote-desktop
Remote desktop support for google-chrome & chromium.
%endif

%prep
%if %{with normalsource}
%setup -n chromium-%{version} 
%else
wget -c https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
tar xJf %{_builddir}/chromium-%{version}.tar.xz -C %{_builddir}
%setup -T -D -n chromium-%{version} 
%endif

# Our cool project
sed -i 's|Developer Build|UnitedRPMs Build|' components/version_ui_strings.grdp

%if %{with clang_bundle}
tar xJf %{S:23} -C %{_builddir}
pushd %{_builddir}
mv -f clang+llvm-11.0.0-x86_64-linux-gnu-ubuntu-20.04 buclang 
pushd buclang/lib/
ln -sf /usr/lib64/libz3.so.0.0.0 libz3.so.4.8
popd
 popd
%endif

# V8 fix
# src/third_party/siphash/halfsiphash.h is missed
#rm -rf v8/
#tar xmzvf %{S:24} -C $PWD
#mv -f v8-7.5.48 v8

# Unpack fonts
# Chromium why does not include it?
mkdir -p third_party/test_fonts/test_fonts
tar xmzvf %{S:17} -C third_party/test_fonts
tar xmzvf %{S:19} -C third_party/test_fonts/test_fonts
cp -f third_party/test_fonts/LICENSE third_party/test_fonts/test_fonts/
# git clone --depth 1 https://github.com/google/fonts.git
# Arimo
tar xJf %{S:20} -C third_party/test_fonts/test_fonts
# cousine
tar xJf %{S:21} -C third_party/test_fonts/test_fonts
#
pushd third_party/test_fonts/test_fonts
unzip %{S:15}
tar xf %{S:16}
mv MuktiNarrow0.94/MuktiNarrow.ttf .
rm -rf MuktiNarrow0.94
%if 0%{?fedora} >= 32
cp -a /usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf /usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf .
%else
cp -a /usr/share/fonts/dejavu/DejaVuSans.ttf /usr/share/fonts/dejavu/DejaVuSans-Bold.ttf .
%endif
cp -a %{S:14} .  
cp -a /usr/share/fonts/lohit-devanagari/Lohit-Devanagari.ttf /usr/share/fonts/lohit-gurmukhi/Lohit-Gurmukhi.ttf /usr/share/fonts/lohit-tamil/Lohit-Tamil.ttf .
cp -a /usr/share/fonts/google-noto-cjk/NotoSansCJKjp-Regular.otf /usr/share/fonts/google-noto/NotoSansKhmer-Regular.ttf .
%if 0%{?fedora} >= 33
cp -a  /usr/share/fonts/google-tinos-fonts/Tinos-*.ttf .
%else
cp -a /usr/share/fonts/google-croscore/Tinos-*.ttf .
%endif
cp -f %{S:18} .
#svn checkout --force https://github.com/google/fonts/trunk/apache/arimo . && rm -rf .svn 
#svn checkout --force https://github.com/google/fonts/trunk/apache/cousine . && rm -rf .svn
popd
#

# Copy the toolchain settings
mkdir toolchain
cp %{S:2} toolchain/BUILD.gn

%if %{with system_markupsafe}
pushd third_party/
rm -rf markupsafe/
ln -sf %{python2_sitearch}/markupsafe/ markupsafe
popd
%endif


#pushd third_party
#rm -rf markupsafe/
#mkdir -p markupsafe
#tar xmzvf %{S:22} -C $PWD/
# git clone --depth 1 https://github.com/pallets/markupsafe.git $PWD/markupsafe
#cp -f $PWD/markupsafe-1.1.1/src/markupsafe/*.py $PWD/markupsafe/
#cp -f $PWD/markupsafe-1.1.1/src/markupsafe/*.c $PWD/markupsafe/
#popd


# node fix
mkdir -p third_party/node/linux/node-linux-x64/bin/
pushd third_party/node/linux/node-linux-x64/bin/
rm -f node
ln -sf /usr/bin/node node
popd

%if %{with remote_desktop}
# Fix hardcoded path in remoting code
sed -i 's|/opt/google/chrome-remote-desktop|%{crd_path}|g' remoting/host/setup/daemon_controller_delegate_linux.cc
%endif

# https://groups.google.com/a/chromium.org/d/msg/chromium-packagers/wuInaKJkosg/kMfIV_7wDgAJ
#rm -rf third_party/freetype/src
#git clone https://chromium.googlesource.com/chromium/src/third_party/freetype2 third_party/freetype/src 

# xlocale.h is gone in F26/RAWHIDE
sed -r -i 's/xlocale.h/locale.h/' buildtools/third_party/libc++/trunk/include/__locale

# Allow building against system libraries in official builds
  sed -i 's/OFFICIAL_BUILD/GOOGLE_CHROME_BUILD/' \
    tools/generate_shim_headers/generate_shim_headers.py


# Avoid CFI failures with unbundled libxml
  sed -i -e 's/\<xmlMalloc\>/malloc/' -e 's/\<xmlFree\>/free/' \
    third_party/blink/renderer/core/xml/*.cc \
    third_party/blink/renderer/core/xml/parser/xml_document_parser.cc \
    third_party/libxml/chromium/libxml_utils.cc

# Patches, disabled autosetup

#patch12 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
#patch6 -p1
#patch7 -p1
#patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
#patch16 -p1
%patch17 -p1

%if %{with gtk2}
%patch22 -p1
%endif


# Change shebang in all relevant files in this directory and all subdirectories
# See `man find` for how the `-exec command {} +` syntax works
# find -type f -exec sed -iE '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python2}=' {} +
find -depth -type f -writable -name "*.py" -exec sed -iE '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python2}=' {} +

# HEVC support
cp -f third_party/ffmpeg/libavcodec/hevcdec.c third_party/ffmpeg/libavcodec/autorename_libavcodec_hevcdec.c
cp -f third_party/ffmpeg/libavformat/hevc.c  third_party/ffmpeg/libavformat/autorename_libavformat_hevc.c

sed -i 's|define CONFIG_HEVC_DECODER 0|define CONFIG_HEVC_DECODER 1|g' third_party/ffmpeg/chromium/config/Chrome/linux/x64/config.h
sed -i 's|define CONFIG_HEVC_PARSER 0|define CONFIG_HEVC_PARSER 1|g' third_party/ffmpeg/chromium/config/Chrome/linux/x64/config.h
sed -i 's|define CONFIG_HEVC_DEMUXER 0|define CONFIG_HEVC_DEMUXER 1|g' third_party/ffmpeg/chromium/config/Chrome/linux/x64/config.h
#

# python2 fix
mkdir -p "$HOME/bin/"
ln -sfn %{__python2} $HOME/bin/python
export PATH="$HOME/bin/:$PATH"

python2 build/linux/unbundle/remove_bundled_libraries.py --do-remove \
    base/third_party/cityhash \
    base/third_party/double_conversion/double-conversion \
    base/third_party/dynamic_annotations \
    base/third_party/icu \
    base/third_party/nspr \
    base/third_party/superfasthash \
    base/third_party/symbolize \
    base/third_party/valgrind \
    base/third_party/xdg_mime \
    base/third_party/xdg_user_dirs \
    buildtools/third_party/libc++ \
    buildtools/third_party/libc++abi \
    chrome/third_party/mozilla_security_manager \
    courgette/third_party \
    net/third_party/mozilla_security_manager \
    net/third_party/nss \
    net/third_party/quiche \
    net/third_party/uri_template \
    third_party/abseil-cpp \
    third_party/angle \
    third_party/angle/src/common/third_party/base \
    third_party/angle/src/common/third_party/smhasher \
    third_party/angle/src/common/third_party/xxhash \
    third_party/angle/src/third_party/compiler \
    third_party/angle/src/third_party/libXNVCtrl \
    third_party/angle/src/third_party/trace_event \
    third_party/angle/src/third_party/volk \
    third_party/angle/third_party/glslang \
    third_party/angle/third_party/spirv-headers \
    third_party/angle/third_party/spirv-tools \
    third_party/angle/third_party/vulkan-headers \
    third_party/angle/third_party/vulkan-loader \
    third_party/angle/third_party/vulkan-tools \
    third_party/angle/third_party/vulkan-validation-layers \
    third_party/apple_apsl \
    third_party/axe-core \
    third_party/blink \
    third_party/boringssl \
    third_party/boringssl/src/third_party/fiat \
    third_party/breakpad \
    third_party/breakpad/breakpad/src/third_party/curl \
    third_party/brotli \
    third_party/catapult \
    third_party/catapult/common/py_vulcanize/third_party/rcssmin \
    third_party/catapult/common/py_vulcanize/third_party/rjsmin \
    third_party/catapult/third_party/polymer \
    third_party/catapult/tracing/third_party/d3 \
    third_party/catapult/tracing/third_party/gl-matrix \
    third_party/catapult/tracing/third_party/jpeg-js \
    third_party/catapult/tracing/third_party/jszip \
    third_party/catapult/tracing/third_party/mannwhitneyu \
    third_party/catapult/tracing/third_party/oboe \
    third_party/catapult/tracing/third_party/pako \
    third_party/ced \
    third_party/cld_3 \
    third_party/closure_compiler \
    third_party/crashpad \
    third_party/crashpad/crashpad/third_party/lss \
    third_party/crashpad/crashpad/third_party/zlib \
    third_party/crc32c \
    third_party/cros_system_api \
    third_party/dav1d \
    third_party/dawn \
    third_party/depot_tools \
    third_party/devscripts \
    third_party/devtools-frontend \
    third_party/devtools-frontend/src/front_end/third_party/acorn \
    third_party/devtools-frontend/src/front_end/third_party/chromium \
    third_party/devtools-frontend/src/front_end/third_party/codemirror \
    third_party/devtools-frontend/src/front_end/third_party/i18n \
    third_party/devtools-frontend/src/front_end/third_party/fabricjs \
    third_party/devtools-frontend/src/front_end/third_party/intl-messageformat \
    third_party/devtools-frontend/src/front_end/third_party/lighthouse \
    third_party/devtools-frontend/src/front_end/third_party/lit-html \
    third_party/devtools-frontend/src/front_end/third_party/lodash-isequal \
    third_party/devtools-frontend/src/front_end/third_party/marked \
    third_party/devtools-frontend/src/front_end/third_party/wasmparser \
    third_party/devtools-frontend/src/third_party \
    third_party/dom_distiller_js \
    third_party/emoji-segmenter \
    third_party/flatbuffers \
    third_party/freetype \
    third_party/libgifcodec \
    third_party/google_input_tools \
    third_party/google_input_tools/third_party/closure_library \
    third_party/google_input_tools/third_party/closure_library/third_party/closure \
    third_party/googletest \
    third_party/glslang \
    third_party/hunspell \
    third_party/iccjpeg \
    third_party/icu \
    third_party/inspector_protocol \
    third_party/jsoncpp \
    third_party/jstemplate \
    third_party/khronos \
    third_party/leveldatabase \
    third_party/libXNVCtrl \
    third_party/libaddressinput \
    third_party/libaom \
    third_party/libaom/source/libaom/third_party/vector \
    third_party/libaom/source/libaom/third_party/x86inc \
    third_party/libavif \
    third_party/libjingle \
    third_party/libphonenumber \
    third_party/libsecret \
    third_party/libsrtp \
    third_party/libsync \
    third_party/libudev \
    third_party/libwebm \
    third_party/libyuv \
    third_party/llvm \
    third_party/lottie \
    third_party/lss \
    third_party/lzma_sdk \
    third_party/mako \
    third_party/metrics_proto \
    third_party/modp_b64 \
    third_party/nasm \
    third_party/nearby \
    third_party/node \
    third_party/node/node_modules/polymer-bundler/lib/third_party/UglifyJS2 \
    third_party/one_euro_filter \
    third_party/opencv \
    third_party/openscreen \
    third_party/openscreen/src/third_party/mozilla \
    third_party/openscreen/src/third_party/tinycbor \
    third_party/ots \
    third_party/perfetto \
    third_party/pdfium \
    third_party/pdfium/third_party/agg23 \
    third_party/pdfium/third_party/base \
    third_party/pdfium/third_party/bigint \
    third_party/pdfium/third_party/freetype \
    third_party/pdfium/third_party/lcms \
    third_party/pdfium/third_party/libopenjpeg20 \
    third_party/pdfium/third_party/libpng16 \
    third_party/pdfium/third_party/libtiff \
    third_party/pdfium/third_party/skia_shared \
    third_party/pffft \
    third_party/polymer \
    third_party/private-join-and-compute \
    third_party/protobuf \
    third_party/protobuf/third_party/six \
    third_party/pyjson5/src/json5 \
    third_party/qcms \
    third_party/rnnoise \
    third_party/s2cellid \
    third_party/schema_org \
    third_party/securemessage \
    third_party/simplejson \
    third_party/skia \
    third_party/skia/include/third_party/skcms \
    third_party/skia/include/third_party/vulkan/vulkan \
    third_party/skia/third_party/skcms \
    third_party/skia/third_party/vulkanmemoryallocator \
    third_party/smhasher \
    third_party/spirv-headers \
    third_party/SPIRV-Tools \
    third_party/sqlite \
    third_party/swiftshader \
    third_party/swiftshader/third_party/astc-encoder \
    third_party/swiftshader/third_party/llvm-subzero \
    third_party/swiftshader/third_party/marl \
    third_party/swiftshader/third_party/SPIRV-Headers \
    third_party/swiftshader/third_party/subzero \
    third_party/tcmalloc \
    third_party/ukey2 \
    third_party/unrar \
    third_party/usrsctp \
    third_party/vulkan \
    third_party/web-animations-js \
    third_party/webdriver \
    third_party/webrtc \
    third_party/webrtc/common_audio/third_party/ooura \
    third_party/webrtc/common_audio/third_party/spl_sqrt_floor \
    third_party/webrtc/modules/third_party/fft \
    third_party/webrtc/modules/third_party/g711 \
    third_party/webrtc/modules/third_party/g722 \
    third_party/webrtc/rtc_base/third_party/base64 \
    third_party/webrtc/rtc_base/third_party/sigslot \
    third_party/widevine \
    third_party/woff2 \
    third_party/wuffs \
    third_party/xcbproto \
    third_party/zxcvbn-cpp \
    third_party/zlib/google \
    url/third_party/mozilla \
    v8/src/third_party/siphash \
    v8/src/third_party/utf8-decoder \
    v8/src/third_party/valgrind \
    v8/third_party/inspector_protocol \
    v8/third_party/v8 \
    third_party/adobe \
    third_party/speech-dispatcher \
    third_party/usb_ids \
    third_party/xdg-utils \
    tools/gn/src/base/third_party/icu \
    third_party/libvpx \
    third_party/libvpx/source/libvpx/third_party/x86inc \
    third_party/catapult/third_party/six \
    third_party/protobuf/third_party/six \
    tools/grit/third_party/six \
    third_party/catapult/third_party/beautifulsoup4 \
    third_party/catapult/third_party/html5lib-python \
%if !%{with re2_external}
		third_party/re2 \
%endif
%if %{with remote_desktop}
		third_party/sinonjs \
		third_party/blanketjs \
		third_party/qunit \
%endif
%if !%{with system_jinja2}
    		third_party/jinja2 \
%endif
%if %{with system_libxml2}
   		third_party/libxml/chromium \
%else
    		third_party/libxml \
%endif
%if !%{with system_markupsafe}
		third_party/markupsafe \
%endif
%if !%{with system_openh264}
    		third_party/openh264 \
%endif
%if !%{with system_ply}
    		third_party/ply \
%endif
%if !%{with system_harfbuzz}
    		third_party/harfbuzz-ng \
%endif
%if !%{with system_ffmpeg} 
		third_party/ffmpeg 
%endif

python2 build/linux/unbundle/replace_gn_files.py --system-libraries \
%if %{with system_ffmpeg}
    ffmpeg \
%endif
    flac \
    libdrm \
    libevent \
%if %{with system_harfbuzz}
    harfbuzz-ng \
%endif
    libjpeg \
    libpng \
    libwebp \
%if %{with system_libxml2}
    libxml \
%endif
    libxslt \
%if %{with system_openh264}
    openh264 \
%endif
    snappy \
%if %{with re2_external}
    re2 \
%endif
%if %{with system_libicu}
    icu \
%endif
    opus \
    fontconfig \
    zlib


# Don't use static libstdc++
#sed -i '/-static-libstdc++/d' tools/gn/build/gen.py

%if %{with system_jinja2}
rm -rf third_party/jinja2 
ln -s %{python2_sitelib}/jinja2 third_party/jinja2
%endif

%if %{with system_ply}
rm -rf third_party/ply
ln -s %{python2_sitelib}/ply third_party/ply
%endif


%if 0%{?fedora} >= 28 || %{with clang_bundle}
sed -i \
    -e '/"--fsplit-lto-unit"/d' build/config/compiler/BUILD.gn

sed -i \
    -e '/"-Wno-defaulted-function-deleted"/d' build/config/compiler/BUILD.gn

sed -i \
    -e '/"-Wextra-semi-stmt"/d' build/config/compiler/BUILD.gn

sed -i \
    -e '/"-Wno-implicit-int-float-conversion"/d' build/config/compiler/BUILD.gn

sed -i \
    -e '/"-Wno-c99-designator"/d' build/config/compiler/BUILD.gn

sed -i \
    -e '/"-Wno-final-dtor-non-final-class"/d' build/config/compiler/BUILD.gn

sed -i \
    -e '/"-Wno-sizeof-array-div"/d' build/config/compiler/BUILD.gn
    
sed -i \
    -e '/"-Wno-bitwise-conditional-parentheses"/d' build/config/compiler/BUILD.gn 
    
sed -i \
    -e '/"-Wno-builtin-assume-aligned-alignment"/d' build/config/compiler/BUILD.gn 
    
sed -i \
    -e '/"-Wno-deprecated-copy"/d' build/config/compiler/BUILD.gn
    
sed -i \
    -e '/"-Wno-misleading-indentation"/d' build/config/compiler/BUILD.gn    
    
sed -i \
    -e '/"-Wno-non-c-typedef-for-linkage"/d' build/config/compiler/BUILD.gn 
    
sed -i \
    -e '/"-Wno-psabi"/d' build/config/compiler/BUILD.gn    
    
sed -i \
    -e '/"-Wno-string-concatenation"/d' build/config/compiler/BUILD.gn 
    
sed -i \
    -e '/"-Wextra-tokens"/d' build/config/compiler/BUILD.gn   

sed -i \
    -e '/"-Wmax-tokens"/d' build/config/compiler/BUILD.gn           
      
sed -i \
    -e '/"-Wno-enum-float-conversion"/d' build/config/compiler/BUILD.gn           
            
sed -i \
    -e '/"-Qunused-arguments"/d' \
    build/config/compiler/BUILD.gn

%endif


%build

# python2 fix
export PATH="$HOME/bin/:$PATH"

# some still call gcc/g++
%if %{with clang}
%if %{with clang_bundle}
export CC=%{_builddir}/buclang/bin/clang
export CXX=%{_builddir}/buclang/bin/clang++
export LD_LIBRARY_PATH=%{_builddir}/buclang/lib:%{_libdir}:$LD_LIBRARY_PATH
export CFLAGS="-O4 -I%{_builddir}/buclang/include -fPIC"
export CXXFLAGS="-O4 -I%{_builddir}/buclang/include -fPIC"
export LDFLAGS="-O4 -L%{_builddir}/buclang/lib"
%else
export CC=clang
export CXX=clang++
export LD=lld
%endif
mkdir -p "$HOME/bin/"
ln -sfn $CC $HOME/bin/gcc
ln -sfn $CXX $HOME/bin/g++
export PATH="$HOME/bin/:$PATH"
%else
export CC="gcc"
export CXX="g++"
export CXXFLAGS="$CXXFLAGS -fno-delete-null-pointer-checks"
%endif

export AR=ar NM=nm
export PNACLPYTHON=%{__python2}

# GN conf
_flags+=(
    'is_debug=false'
%if %{with clang}
    'is_clang=true' 
%else
    'is_clang=false' 
%endif
%if %{with clang_bundle}
    'clang_base_path="%{_builddir}/buclang"'
    'clang_use_chrome_plugins=false'
%else
    'clang_base_path="/usr"'
    'clang_use_chrome_plugins=false'
%endif
    'fatal_linker_warnings=false'
    'treat_warnings_as_errors=false'
    'fieldtrial_testing_like_official_build=true'
    'ffmpeg_branding="Chrome"'
    'proprietary_codecs=true'
%if %{with vaapi}
    'use_vaapi=true'
%else
    'use_vaapi=false'
%endif
    'link_pulseaudio=true'
    'use_custom_libcxx=false'
    'use_lld=false'
    'use_allocator="none"'
    'use_cups=true'
    'use_gnome_keyring=false'
    'use_gold=false'
    'use_kerberos=true'
    'use_pulseaudio=true'
    'use_system_freetype=false'
    'use_sysroot=false'
    'enable_hangout_services_extension=true'
    'enable_widevine=true'
    'enable_nacl=false'
%if %{with swiftshader}
    'enable_swiftshader=true'
%else
    'enable_swiftshader=false'
%endif
    "google_api_key=\"AIzaSyD1hTe85_a14kr1Ks8T3Ce75rvbR1_Dx7Q\""
    "google_default_client_id=\"4139804441.apps.googleusercontent.com\""
    "google_default_client_secret=\"KDTRKEZk2jwT_7CDpcmMA--P\""
%if %{with system_ffmpeg}
    'is_component_ffmpeg=true' 
%endif
%if %{with system_harfbuzz}
    'use_system_harfbuzz=true'
%else
    'use_system_harfbuzz=false'
%endif
%if %{with gtk2}
    'gtk_version=2'
%endif
%ifarch x86_64
    'system_libdir="lib64"'
%endif 
    'symbol_level=0'
%if %{with jumbo_unity}
    'use_jumbo_build=true'
    'jumbo_file_merge_limit=8'
%endif
    'remove_webcore_debug_symbols=true'
)


  # Do not warn about unknown warning options
  CFLAGS+='   -Wno-unknown-warning-option'
  CXXFLAGS+=' -Wno-unknown-warning-option'
  
  tools/gn/bootstrap/bootstrap.py -v --no-clean --gn-gen-args="${_flags[*]}"  

# Build files for Ninja #
#unzip %{S:25} -d $PWD
#$PWD/gn 
out/Release/gn gen out/Release --args="${_flags[*]}" --script-executable=/usr/bin/python2   
#gn gen out/Release --args="${_flags[*]}" --script-executable=/usr/bin/python2   


# SUPER POWER!
jobs=$(grep processor /proc/cpuinfo | tail -1 | grep -o '[0-9]*')

%if %{with remote_desktop}
%ninja_build -C out/Release remoting_all -j$jobs
%endif

# HERE the real build
%if %{with devel_tools}
%if %{with system_ffmpeg}
%ninja_build -C out/Release third_party/widevine/cdm media/ffmpeg chrome chrome_sandbox chromedriver -j$jobs 
%else
%ninja_build -C out/Release third_party/widevine/cdm chrome chrome_sandbox chromedriver -j$jobs 
%endif
%else
%if %{with system_ffmpeg}
%ninja_build -C out/Release third_party/widevine/cdm media/ffmpeg chrome -j$jobs 
%else
%ninja_build -C out/Release third_party/widevine/cdm media/ffmpeg chrome -j$jobs 
%endif
%endif

%install

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{chromiumdir}/locales
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_datadir}/appdata
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps
sed -e "s|@LIBDIR@|%{_libdir}|" -e "s|@@BUILDTARGET@@|`cat /etc/redhat-release`|" \
    %{SOURCE10} > chromium-wrapper
install -m 755 chromium-wrapper %{buildroot}%{_bindir}/%{name}
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE11}
install -m 644 %{SOURCE12} %{buildroot}%{_datadir}/gnome-control-center/default-apps/
appstream-util validate-relax --nonet %{SOURCE13}
mkdir -p %{buildroot}%{_datadir}/appdata/
install -m 644 %{SOURCE13} %{buildroot}%{_datadir}/appdata/


# Brute Copy
cp \
    out/Release/{chrome_{100,200}_percent,resources,headless_lib}.pak \
    out/Release/{*.bin,*.so,v8_context_snapshot_generator,mksnapshot,brotli,character_data_generator,xdg-settings,xdg-mime,transport_security_state_generator,torque,nasm,protoc,top_domain_generator,flatc,bytecode_builtins_list_generator} \
    out/Release/{cddl,crashpad_handler,protozero_plugin,cppgen_plugin,generate_colors_info,make_top_domain_list_variables,gen-regexp-special-case} \
    %{buildroot}/%{chromiumdir}/

install -m 755 out/Release/chrome %{buildroot}/%{chromiumdir}/chromium

#locales
mv -f out/Release/locales %{buildroot}/%{chromiumdir}/

# resources
mv -f out/Release/resources %{buildroot}/%{chromiumdir}/

# Media Engagement
mv -f out/Release/MEIPreload %{buildroot}/%{chromiumdir}/

# pyproto
mv -f out/Release/pyproto %{buildroot}/%{chromiumdir}/

# libicu
install -m 644 out/Release/icudtl.dat %{buildroot}/%{chromiumdir}/

# Angle
mv -f out/Release/angledata %{buildroot}/%{chromiumdir}/

# swiftshader
%if %{with swiftshader}
mv -f out/Release/swiftshader %{buildroot}/%{chromiumdir}/
%endif

for size in 24 48 64 128 256; do
    install -Dm644 chrome/app/theme/chromium/product_logo_$size.png \
      %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps/chromium.png
  done

for size in 16 32; do
    install -Dm644 chrome/app/theme/default_100_percent/chromium/product_logo_$size.png \
      %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps/chromium.png
  done

# Manpage
install -Dm644 chrome/app/resources/manpage.1.in \
    %{buildroot}/%{_mandir}/man1/chromium.1

sed -i \
    -e "s/@@MENUNAME@@/Chromium/g" \
    -e "s/@@PACKAGE@@/chromium/g" \
    -e "s/@@USR_BIN_SYMLINK_NAME@@/chromium/g" \
    %{buildroot}/%{_mandir}/man1/chromium.1

mkdir -p %{buildroot}/%{chromiumdir}/PepperFlash

# devel tools
%if %{with devel_tools}
install -m 4755 out/Release/chrome_sandbox %{buildroot}/%{chromiumdir}/chrome-sandbox
install -m 755 out/Release/chromedriver %{buildroot}/%{chromiumdir}/
ln -s %{chromiumdir}/chromedriver %{buildroot}%{_bindir}/%{name}-chromedriver
%endif

%if %{with remote_desktop}
# Remote desktop bits
mkdir -p %{buildroot}%{crd_path}

pushd %{buildroot}%{crd_path}
ln -s %{_libdir}/%{name} lib
popd

# See remoting/host/installer/linux/Makefile for logic
cp -a out/Release/remoting_native_messaging_host %{buildroot}/%{crd_path}/remoting_native_messaging_host
cp -a out/Release/remote_assistance_host %{buildroot}/%{crd_path}/remote-assistance-host
cp -a out/Release/remoting_locales %{buildroot}/%{crd_path}/
cp -a out/Release/remoting_me2me_host %{buildroot}/%{crd_path}/chrome-remote-desktop-host
cp -a out/Release/remoting_start_host %{buildroot}/%{crd_path}/start-host
cp -a out/Release/remoting_user_session %{buildroot}/%{crd_path}/user-session
chmod a+s %{buildroot}/%{crd_path}/user-session

mkdir -p %{buildroot}/%{_sysconfdir}/%{name}/

# chromium
mkdir -p %{buildroot}%{_sysconfdir}/chromium/remoting_native_messaging_host
# google-chrome
mkdir -p %{buildroot}%{_sysconfdir}/opt/chrome/
cp -a out/Release/remoting/* %{buildroot}%{_sysconfdir}/chromium/remoting_native_messaging_host/
for i in %{buildroot}%{_sysconfdir}/chromium/remoting_native_messaging_host/*.json; do
    sed -i 's|/opt/google/chrome-remote-desktop|%{crd_path}|g' $i
done
pushd %{buildroot}%{_sysconfdir}/opt/chrome/
ln -sf ../../chromium/remoting_native_messaging_host remoting_native_messaging_host
popd

mkdir -p %{buildroot}/var/lib/chrome-remote-desktop
touch %{buildroot}/var/lib/chrome-remote-desktop/hashes

mkdir -p %{buildroot}%{_sysconfdir}/pam.d/
pushd %{buildroot}%{_sysconfdir}/pam.d/
ln -sf system-auth chrome-remote-desktop
popd

cp -a remoting/host/linux/linux_me2me_host.py %{buildroot}/%{crd_path}/chrome-remote-desktop
cp -a remoting/host/installer/linux/is-remoting-session %{buildroot}/%{crd_path}/

mkdir -p %{buildroot}/%{_unitdir}
cp -a %{SOURCE33} %{buildroot}%{_unitdir}/
sed -i 's|@@CRD_PATH@@|%{crd_path}|g' %{buildroot}/%{_unitdir}/chrome-remote-desktop.service
%endif

install -Dm644 %{S:3} \
    %{buildroot}/%{_datadir}/drirc.d/10-%{name}.conf

# Mangling fix
# bash
%if %{with remote_desktop}
sed -i 's|/bin/bash|/usr/bin/bash|g' %{buildroot}/usr/lib64/chrome-remote-desktop/is-remoting-session
sed -i 's|/bin/bash|/usr/bin/bash|g' %{buildroot}/%{_sysconfdir}/chromium/remoting_native_messaging_host/chrome-remote-desktop-host
sed -i 's|/bin/bash|/usr/bin/bash|g' %{buildroot}/%{_sysconfdir}/chromium/remoting_native_messaging_host/user-session
%endif
sed -i 's|/bin/sh|/usr/bin/sh|g' %{buildroot}/%{chromiumdir}/xdg-settings
sed -i 's|/bin/sh|/usr/bin/sh|g' %{buildroot}/%{chromiumdir}/xdg-mime
# python
sed -i '1 i\#!/usr/bin/python2'  %{buildroot}/%{chromiumdir}/pyproto/google/protobuf/message.py
sed -i '1 i\#!/usr/bin/python2'  %{buildroot}/%{chromiumdir}/pyproto/google/protobuf/reflection.py
sed -i '1 i\#!/usr/bin/python2'  %{buildroot}/%{chromiumdir}/pyproto/google/protobuf/service_reflection.py
sed -i '1 i\#!/usr/bin/python2'  %{buildroot}/%{chromiumdir}/pyproto/google/protobuf/__init__.py
sed -i '1 i\#!/usr/bin/python2'  %{buildroot}/%{chromiumdir}/pyproto/google/protobuf/internal/type_checkers.py
sed -i '1 i\#!/usr/bin/python2'  %{buildroot}/%{chromiumdir}/pyproto/google/protobuf/internal/wire_format.py
sed -i '1 i\#!/usr/bin/python2'  %{buildroot}/%{chromiumdir}/pyproto/google/protobuf/internal/containers.py
sed -i '1 i\#!/usr/bin/python2'  %{buildroot}/%{chromiumdir}/pyproto/google/protobuf/internal/python_message.py
sed -i '1 i\#!/usr/bin/python2'  %{buildroot}/%{chromiumdir}/pyproto/google/protobuf/internal/api_implementation.py
sed -i '1 i\#!/usr/bin/python2'  %{buildroot}/%{chromiumdir}/pyproto/google/protobuf/internal/decoder.py
sed -i '1 i\#!/usr/bin/python2'  %{buildroot}/%{chromiumdir}/pyproto/google/protobuf/internal/encoder.py
sed -i '1 i\#!/usr/bin/python2'  %{buildroot}/%{chromiumdir}/pyproto/google/protobuf/internal/message_listener.py
sed -i '1 i\#!/usr/bin/python2'  %{buildroot}/%{chromiumdir}/pyproto/google/protobuf/descriptor.py
sed -i '1 i\#!/usr/bin/python2'  %{buildroot}/%{chromiumdir}/pyproto/google/protobuf/service.py
sed -i '1 i\#!/usr/bin/python2'  %{buildroot}/%{chromiumdir}/pyproto/google/protobuf/text_format.py
sed -i '1 i\#!/usr/bin/python2'	 %{buildroot}/%{chromiumdir}/pyproto/google/protobuf/internal/_parameterized.py

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%if %{with remote_desktop}
%pre -n chrome-remote-desktop
getent group chrome-remote-desktop >/dev/null || groupadd -r chrome-remote-desktop

%post -n chrome-remote-desktop
%systemd_post chrome-remote-desktop.service

%preun -n chrome-remote-desktop
%systemd_preun chrome-remote-desktop.service

%postun -n chrome-remote-desktop
%systemd_postun_with_restart chrome-remote-desktop.service
%endif

%files
%license LICENSE
%doc AUTHORS 
%{_bindir}/%{name}
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/gnome-control-center/default-apps/%{name}.xml
%{_datadir}/icons/hicolor/*/apps/chromium.png
%{_mandir}/man1/chromium.1.gz
%dir %{chromiumdir}
%{chromiumdir}/chromium
%if %{with devel_tools}
%{chromiumdir}/chromedriver
%{chromiumdir}/chrome-sandbox
%endif
%if !%{with system_libicu}
%{chromiumdir}/icudtl.dat
%endif

%{chromiumdir}/snapshot_blob.bin
%{chromiumdir}/*.pak
%dir %{chromiumdir}/PepperFlash/

# new
%{chromiumdir}/MEIPreload/
%{chromiumdir}/angledata/
%{chromiumdir}/brotli
%{chromiumdir}/character_data_generator
%{chromiumdir}/locales/
%{chromiumdir}/mksnapshot
%{chromiumdir}/pyproto/
%{chromiumdir}/resources/inspector/
%{chromiumdir}/resources/inspector_overlay/
%if %{with swiftshader}
%{chromiumdir}/swiftshader/
%endif
%{chromiumdir}/transport_security_state_generator
%{chromiumdir}/v8_context_snapshot.bin
%{chromiumdir}/v8_context_snapshot_generator
%{chromiumdir}/xdg-mime
%{chromiumdir}/xdg-settings
%{_datadir}/drirc.d/10-%{name}.conf
%{chromiumdir}/bytecode_builtins_list_generator
%{chromiumdir}/flatc
%{chromiumdir}/nasm
%{chromiumdir}/protoc
%{chromiumdir}/top_domain_generator
%{chromiumdir}/torque
%{chromiumdir}/cddl
%{chromiumdir}/cppgen_plugin
%{chromiumdir}/crashpad_handler
%{chromiumdir}/gen-regexp-special-case
%{chromiumdir}/generate_colors_info
%{chromiumdir}/make_top_domain_list_variables
%{chromiumdir}/protozero_plugin

%files libs
%{chromiumdir}/lib*.so*

%if !%{with system_ffmpeg}
%exclude %{chromiumdir}/libffmpeg.so
%endif

%if %{with devel_tools}
%files chromedriver
%doc AUTHORS
%license LICENSE
%{_bindir}/%{name}-chromedriver
%{chromiumdir}/chromedriver
%endif

%if !%{with system_ffmpeg}
%files libs-media
%{chromiumdir}/libffmpeg.so*
# {chromiumdir}/libmedia.so*
%endif

%if %{with remote_desktop}
%files -n chrome-remote-desktop
%{crd_path}/chrome-remote-desktop
%{crd_path}/chrome-remote-desktop-host
%{crd_path}/is-remoting-session
%{crd_path}/lib
%{crd_path}/remoting_native_messaging_host
%{crd_path}/remote-assistance-host
%{_sysconfdir}/pam.d/chrome-remote-desktop
%{_sysconfdir}/chromium/remoting_native_messaging_host/
%{_sysconfdir}/opt/chrome/
%{crd_path}/remoting_locales/
%{crd_path}/start-host
%{crd_path}/user-session
%{_unitdir}/chrome-remote-desktop.service
/var/lib/chrome-remote-desktop/
%endif

%changelog

* Sat Oct 24 2020 - David Va <davidva AT tuta DOT io> 86.0.4240.111
- Updated to 86.0.4240.111

* Fri Oct 23 2020 - David Va <davidva AT tuta DOT io> 86.0.4240.75
- Updated to 86.0.4240.75

* Wed Jul 15 2020 - David Va <davidva AT tuta DOT io> 83.0.4103.116
- Updated to 83.0.4103.116

* Mon Jun 22 2020 - David Va <davidva AT tuta DOT io> 83.0.4103.106
- Updated to 83.0.4103.106

* Mon Jun 08 2020 - David Va <davidva AT tuta DOT io> 83.0.4103.97-19.1
- Updated to 83.0.4103.97

* Fri May 29 2020 - David Va <davidva AT tuta DOT io> 81.0.4044.138-607.1
- Rebuilt

* Mon May 25 2020 - David Va <davidva AT tuta DOT io> 81.0.4044.138-606.1
- Rebuilt for ffmpeg and openh264

* Tue May 12 2020 - David Va <davidva AT tuta DOT io> 81.0.4044.138
- Updated to 81.0.4044.138

* Sun Apr 12 2020 - David Va <davidva AT tuta DOT io> 81.0.4044.92
- Updated to 81.0.4044.92

* Sun Apr 05 2020 - David Va <davidva AT tuta DOT io> 80.0.3987.163
- Updated to 80.0.3987.163

* Wed Mar 18 2020 - David Va <davidva AT tuta DOT io> 80.0.3987.149
- Updated to 80.0.3987.149

* Wed Jan 29 2020 - David Va <davidva AT tuta DOT io> 80.0.3987.87
- Updated to 80.0.3987.87

* Tue Jan 21 2020 - David Va <davidva AT tuta DOT io> 80.0.3964.0
- Updated to 80.0.3964.0

* Thu Nov 28 2019 - David Va <davidva AT tuta DOT io> 78.0.3904.108
- Updated to 78.0.3904.108

* Thu Nov 07 2019 - David Va <davidva AT tuta DOT io> 78.0.3904.97
- Updated to 78.0.3904.97

* Thu Sep 19 2019 - David Va <davidva AT tuta DOT io> 77.0.3865.90
- Updated to 77.0.3865.90

* Sat Jul 20 2019 - David Va <davidva AT tuta DOT io> 75.0.3770.142
- Updated to 75.0.3770.142

* Sun Jun 23 2019 - David Va <davidva AT tuta DOT io> 75.0.3770.100
- Updated to 75.0.3770.100

* Fri May 17 2019 - David Va <davidva AT tuta DOT io> 74.0.3729.157
- Updated to 74.0.3729.157

* Wed May 01 2019 - David Va <davidva AT tuta DOT io> 74.0.3729.131
- Updated to 74.0.3729.131

* Fri Apr 26 2019 - David Va <davidva AT tuta DOT io> 74.0.3729.108-200.1
- Updated to 74.0.3729.108

* Wed Mar 13 2019 - David Va <davidva AT tuta DOT io> 73.0.3683.86-123.1
- Updated to 73.0.3683.86

* Mon Mar 04 2019 - David Va <davidva AT tuta DOT io> 72.0.3626.121-7
- Updated to 72.0.3626.121

* Sat Dec 22 2018 - David Va <davidva AT tuta DOT io> 71.0.3578.98-7
- Updated to 71.0.3578.98
- Widevine fix and conditional path in local (friendly with snaps and maybe flatpak)

* Fri Nov 30 2018 - David Va <davidva AT tuta DOT io> 70.0.3538.102-7
- Updated to 70.0.3538.110
- Tweaks enabled

* Fri Nov 16 2018 - David Va <davidva AT tuta DOT io> 70.0.3538.102-7
- Updated to 70.0.3538.102

* Wed Oct 17 2018 - David Va <davidva AT tuta DOT io> 70.0.3538.67-7
- Updated to 70.0.3538.67

* Wed Oct 03 2018 - David Va <davidva AT tuta DOT io> 69.0.3497.100-8
- Optimization enabled

* Fri Sep 21 2018 - David Va <davidva AT tuta DOT io> 69.0.3497.100-7
- Updated to 69.0.3497.100-7

* Thu Jul 26 2018 - David Va <davidva AT tuta DOT io> 68.0.3440.75-7
- Updated to 68.0.3440.75-7

* Thu Jun 14 2018 - David Vasquez <davidjeremias82 AT gmail DOT com>  67.0.3396.87-3
- Updated to 67.0.3396.87

* Wed Jun 06 2018 - David Vasquez <davidjeremias82 AT gmail DOT com>  67.0.3396.79-3
- Updated to 67.0.3396.79

* Wed May 16 2018 - David Vasquez <davidjeremias82 AT gmail DOT com>  66.0.3359.181-2
- Updated to 66.0.3359.181

* Wed May 09 2018 - David Vasquez <davidjeremias82 AT gmail DOT com>  66.0.3359.170-7
- Updated to 66.0.3359.170

* Wed Mar 21 2018 - David Vasquez <davidjeremias82 AT gmail DOT com>  65.0.3325.181-2
- Updated to 65.0.3325.181

* Thu Feb 01 2018 - David Vasquez <davidjeremias82 AT gmail DOT com>  64.0.3282.140-2
- Updated to 64.0.3282.140

* Tue Jan 09 2018 - David Vasquez <davidjeremias82 AT gmail DOT com>  63.0.3239.132-2
- Updated to 63.0.3239.132

* Thu Dec 14 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  63.0.3239.108-2
- Updated to 63.0.3239.108

* Tue Nov 21 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  62.0.3202.94-2
- Updated to 62.0.3202.94

* Wed Oct 18 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  62.0.3202.62-2
- Updated to 62.0.3202.62

* Fri Sep 15 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  61.0.3163.91-2
- Updated to 61.0.3163.91

* Wed Aug 30 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  60.0.3112.113-2
- Updated to 60.0.3112.113
- LD_PRELOAD fix thanks to domo141

* Wed Aug 16 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  60.0.3112.101-2
- Updated to 60.0.3112.101

* Thu Aug 03 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  60.0.3112.90-2
- Updated to 60.0.3112.90-2

* Sat Jul 08 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  59.0.3071.115-2
- Updated to 59.0.3071.115

* Tue Jun 20 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  59.0.3071.109-2
- Updated to 59.0.3071.109

* Wed May 10 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  58.0.3029.110-2
- Updated to 58.0.3029.110

* Fri May 05 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  58.0.3029.96-2
- Updated to 58.0.3029.96

* Sat Apr 08 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  57.0.2987.133-2
- Updated to 57.0.2987.133

* Tue Mar 28 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  57.0.2987.98-2
- Updated to 57.0.2987.110

* Fri Mar 10 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  57.0.2987.98-2
- Updated to 57.0.2987.98-2

* Thu Mar 02 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  56.0.2924.87-4
- Fix issue with compilation on gcc7, Thanks to Ben Noordhuis

* Mon Feb 06 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  56.0.2924.87-2
- Updated to 56.0.2924.87

* Thu Jan 26 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  56.0.2924.76-2
- Updated to 56.0.2924.76
- Renamed to chromium-freeworld

* Sun Dec 18 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  55.0.2883.87-2
- Updated to 55.0.2883.87

* Fri Dec 02 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  55.0.2883.75-2
- Updated to 55.0.2883.75

* Thu Dec 01 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  54.0.2840.100-3
- Conditional task

* Sat Nov 12 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  54.0.2840.100-2
- Updated to 54.0.2840.100

* Mon Nov 07 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  54.0.2840.90-2
- Updated to 54.0.2840.90

* Mon Oct 31 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  54.0.2840.71-3
- Initial build

