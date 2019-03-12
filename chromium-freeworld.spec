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

%global _python_bytecompile_extra 1
%global chromiumdir %{_libdir}/chromium
%global crd_path %{_libdir}/chrome-remote-desktop
# Do not check any ffmpeg or libmedia bundle files in libdir for requires
%global __requires_exclude_from ^%{chromiumdir}/libffmpeg.*$
%global __requires_exclude_from ^%{chromiumdir}/libmedia.*$


# Generally chromium is a monster if you compile the source code, enabling all; and takes hours compiling; common users doesn't need all tools.
%bcond_without devel_tools
# Chromium users doesn't need chrome-remote-desktop
%bcond_without remote_desktop
#
# Get the version number of latest stable version
# $ curl -s 'https://omahaproxy.appspot.com/all?os=linux&channel=stable' | sed 1d | cut -d , -f 3
%bcond_without normalsource


%global debug_package %{nil}

# clang is necessary for a fast build
%bcond_without clang
# 

# About clang bundle: Necessary in cases where "clang" in system, fails to build chromium.
%if 0%{?fedora} <= 28
%bcond_without clang_bundle
%else
%bcond_with clang_bundle
%endif


# jinja conditional
%if 0%{?fedora} < 26
%bcond_without system_jinja2
%else
%bcond_with system_jinja2
%endif

# markupsafe
%bcond_with system_markupsafe


# https://github.com/dabeaz/ply/issues/66
%if 0%{?fedora} >= 24
%bcond_without system_ply
%else
%bcond_with system_ply
%endif

# Require libxml2 > 2.9.4 for XML_PARSE_NOXXE
%if 0%{?fedora} >= 27
%bcond_without system_libxml2
%else
%bcond_with system_libxml2
%endif

# Component build
# Component build. Setting to true compiles targets declared as "components"
# as shared libraries loaded dynamically. This speeds up development time.
# When false, components will be linked statically.
# For more information see
# https://chromium.googlesource.com/chromium/src/+/master/docs/component_build.md

%bcond_without component_build

# Require harfbuzz >= 1.5.0 for hb_glyph_info_t
%if 0%{?fedora} >= 30
%bcond_without system_harfbuzz
%else
%bcond_with system_harfbuzz
%endif

# Allow testing whether icu can be unbundled
%bcond_with system_libicu

# Allow disabling unconditional build dependency on clang
%bcond_without require_clang

# In UnitedRPMs, we have openh264
%bcond_without system_openh264

# Now is easy to use the external ffmpeg...
%bcond_without system_ffmpeg

# Jumbo / Unity builds
# https://chromium.googlesource.com/chromium/src/+/lkcr/docs/jumbo.md
%bcond_without jumbo_unity

# Vaapi conditional
%bcond_without vaapi

# Gtk2 conditional
%bcond_with gtk2

# re2 conditional
%bcond_with re2_external

Name:       chromium-freeworld
Version:    72.0.3626.121
Release:    7%{?dist}
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
Source15:	https://fontlibrary.org/assets/downloads/gelasio/4d610887ff4d445cbc639aae7828d139/gelasio.zip
Source16:	http://download.savannah.nongnu.org/releases/freebangfont/MuktiNarrow-0.94.tar.bz2
Source17:	https://chromium.googlesource.com/chromium/src.git/+archive/refs/heads/master/third_party/test_fonts.tar.gz
Source18:	https://github.com/web-platform-tests/wpt/raw/master/fonts/Ahem.ttf
Source19:	https://chromium.googlesource.com/chromium/src/+archive/66.0.3359.158/third_party/gardiner_mod.tar.gz
Source20:	https://github.com/UnitedRPMs/chromium-freeworld/releases/download/fonts/arimo.tar.xz
Source21:	https://github.com/UnitedRPMs/chromium-freeworld/releases/download/fonts/cousine.tar.xz

# markupsafe
Source22:	https://github.com/pallets/markupsafe/archive/1.1.1.tar.gz

# Thanks Arch Linux
Patch1:         chromium-widevine.patch
# Thanks Gentoo
Patch2:         chromium-compiler-r7.patch
# Thanks Debian
Patch3:	widevine-locations.patch
# VAAPI
%if %{with vaapi}
Patch4:	chromium-vaapi.patch
Patch5:	chromium-vaapi-relax-the-version-check-for-VA-API.patch
Patch6:	chromium-enable-mojo-video-decoders-by-default.patch
Patch7:	chromium-vaapi-fix-the-VA_CHECK_VERSION.patch
%endif
Patch8: chromium-skia-harmony.patch
Patch9: chromium-webrtc-missing-header.patch
Patch10: chromium-bootstrap-python2.patch
Patch11: chromium-nacl-llvm-ar.patch
Patch12: chromium-system-icu.patch

ExclusiveArch: x86_64 

# Make sure we don't encounter GCC 5.1 bug
%if 0%{?fedora} >= 22
BuildRequires:	gcc-c++
%endif

%if %{with clang} || %{with require_clang} 
BuildRequires: clang llvm
%endif
# Basic tools and libraries
BuildRequires: ninja-build 
BuildRequires: bison 
BuildRequires: gperf 
BuildRequires: hwdata 
BuildRequires: gn 
BuildRequires: xz
BuildRequires: libgcc(x86-32) 
BuildRequires: glibc(x86-32) 
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
BuildRequires: pkgconfig(xtst) 
BuildRequires: pkgconfig(xscrnsaver)
BuildRequires: pkgconfig(dbus-1) 
BuildRequires: pkgconfig(libudev)
#BuildRequires: pkgconfig(gnome-keyring-1)
BuildRequires: pkgconfig(libffi)
# remove_bundled_libraries.py --do-remove
BuildRequires: python2-rpm-macros
BuildRequires: python-beautifulsoup4
BuildRequires: python-html5lib
%if %{with system_jinja2}
%if 0%{?fedora} >= 24
BuildRequires: python2-jinja2
%else
BuildRequires: python-jinja2
%endif
%endif

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
#BuildRequires: libvpx-devel
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
BuildRequires: vulkan-devel
%if %{with system_libicu}
BuildRequires: libicu-devel
%endif
# ffmpeg external conditional
%if %{with system_ffmpeg}
BuildRequires: ffmpeg-devel >= 4.1
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

Obsoletes: chromium 
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
Obsoletes: chromium-libs 

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
Provides: chromium-libs-media-freeworld = %{version}


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
%autosetup -n chromium-%{version} -p1
%else
wget -c https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
tar xJf %{_builddir}/chromium-%{version}.tar.xz -C %{_builddir}
%autosetup -T -D -n chromium-%{version} -p1
%endif


%if %{with clang_bundle}
wget -c http://releases.llvm.org/7.0.0/clang+llvm-7.0.0-x86_64-linux-gnu-ubuntu-16.04.tar.xz
tar xJf clang+llvm-7.0.0-x86_64-linux-gnu-ubuntu-16.04.tar.xz -C %{_builddir} 
pushd %{_builddir}
mv -f clang+llvm-7.0.0-x86_64-linux-gnu-ubuntu-16.04 buclang
popd
%endif

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
cp -a /usr/share/fonts/dejavu/DejaVuSans.ttf /usr/share/fonts/dejavu/DejaVuSans-Bold.ttf .
cp -a /usr/share/fonts/thai-scalable/Garuda.ttf .
cp -a /usr/share/fonts/lohit-devanagari/Lohit-Devanagari.ttf /usr/share/fonts/lohit-gurmukhi/Lohit-Gurmukhi.ttf /usr/share/fonts/lohit-tamil/Lohit-Tamil.ttf .
cp -a /usr/share/fonts/google-noto-cjk/NotoSansCJKjp-Regular.otf /usr/share/fonts/google-noto/NotoSansKhmer-Regular.ttf .
cp -a /usr/share/fonts/google-croscore/Tinos-*.ttf .
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
%else
pushd third_party
rm -rf markupsafe/
mkdir -p markupsafe
tar xmzvf %{S:22} -C $PWD/
# git clone --depth 1 https://github.com/pallets/markupsafe.git $PWD/markupsafe
cp -f $PWD/markupsafe-1.1.1/src/markupsafe/*.py $PWD/markupsafe/
cp -f $PWD/markupsafe-1.1.1/src/markupsafe/*.c $PWD/markupsafe/
popd
%endif

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

# Change shebang in all relevant files in this directory and all subdirectories
# See `man find` for how the `-exec command {} +` syntax works
# find -type f -exec sed -iE '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python2}=' {} +


# Avoid CFI failures with unbundled libxml
  sed -i -e 's/\<xmlMalloc\>/malloc/' -e 's/\<xmlFree\>/free/' \
    third_party/blink/renderer/core/xml/*.cc \
    third_party/blink/renderer/core/xml/parser/xml_document_parser.cc \
    third_party/libxml/chromium/libxml_utils.cc


# python2 fix
mkdir -p "$HOME/bin/"
ln -sfn /usr/bin/python2.7 $HOME/bin/python
export PATH="$HOME/bin/:$PATH"

python2 build/linux/unbundle/remove_bundled_libraries.py --do-remove \
		base/third_party/dmg_fp \
		base/third_party/dynamic_annotations \
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
		net/third_party/http2 \
		net/third_party/mozilla_security_manager \
		net/third_party/nss \
		net/third_party/quic \
		net/third_party/spdy \
                net/third_party/uri_template \
		third_party/abseil-cpp \
		third_party/angle \
		third_party/angle/src/common/third_party/base \
		third_party/angle/src/common/third_party/smhasher \
		third_party/angle/src/third_party/compiler \
		third_party/angle/src/third_party/libXNVCtrl \
		third_party/angle/src/third_party/trace_event \
		third_party/angle/third_party/glslang \
		third_party/angle/third_party/spirv-headers \
		third_party/angle/third_party/spirv-tools \
		third_party/angle/third_party/vulkan-headers \
		third_party/angle/third_party/vulkan-loader \
		third_party/angle/third_party/vulkan-tools \
		third_party/angle/third_party/vulkan-validation-layers \
		third_party/apple_apsl \
		third_party/blink \
		third_party/boringssl \
		third_party/boringssl/src/third_party/fiat \
		third_party/breakpad \
		third_party/breakpad/breakpad/src/third_party/curl \
		third_party/brotli \
		third_party/cacheinvalidation \
		third_party/catapult \
		third_party/catapult/common/py_vulcanize/third_party/rcssmin \
		third_party/catapult/common/py_vulcanize/third_party/rjsmin \
		third_party/catapult/third_party/beautifulsoup4 \
		third_party/catapult/third_party/html5lib-python \
		third_party/catapult/third_party/polymer \
		third_party/catapult/third_party/six \
		third_party/catapult/tracing/third_party/d3 \
		third_party/catapult/tracing/third_party/gl-matrix \
		third_party/catapult/tracing/third_party/jszip \
		third_party/catapult/tracing/third_party/mannwhitneyu \
		third_party/catapult/tracing/third_party/oboe \
		third_party/catapult/tracing/third_party/pako \
		third_party/ced \
		third_party/cld_3 \
		third_party/closure_compiler \
		third_party/crashpad \
		third_party/crashpad/crashpad/third_party/zlib \
		third_party/crc32c \
		third_party/cros_system_api \
		third_party/devscripts \
		third_party/dom_distiller_js \
		third_party/fips181 \
		third_party/flatbuffers \
		third_party/flot \
		third_party/freetype \
		third_party/google_input_tools \
		third_party/google_input_tools/third_party/closure_library \
		third_party/google_input_tools/third_party/closure_library/third_party/closure \
		third_party/googletest \
		third_party/hunspell \
		third_party/iccjpeg \
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
		third_party/libjingle \
		third_party/libphonenumber \
		third_party/libsecret \
		third_party/libsrtp \
		third_party/libsync \
		third_party/libudev \
		third_party/libwebm \
		third_party/libxml/chromium \
		third_party/libyuv \
		third_party/llvm \
		third_party/lss \
		third_party/lzma_sdk \
		third_party/mesa \
		third_party/metrics_proto \
		third_party/modp_b64 \
		third_party/nasm \
		third_party/node \
		third_party/node/node_modules/polymer-bundler/lib/third_party/UglifyJS2 \
		third_party/openmax_dl \
		third_party/ots \
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
		third_party/perfetto \
		third_party/polymer \
		third_party/protobuf \
		third_party/protobuf/third_party/six \
		third_party/pyjson5 \
		third_party/qcms \
		third_party/rnnoise \
		third_party/s2cellid \
		third_party/sfntly \
		third_party/simplejson \
		third_party/skia \
		third_party/skia/third_party/gif \
		third_party/skia/third_party/skcms \
		third_party/skia/third_party/vulkan \
		third_party/smhasher \
		third_party/spirv-headers \
		third_party/SPIRV-Tools \
		third_party/sqlite \
		third_party/swiftshader \
		third_party/swiftshader/third_party/llvm-subzero \
		third_party/swiftshader/third_party/subzero \
		third_party/unrar \
		third_party/usrsctp \
		third_party/vulkan \
		third_party/web-animations-js \
		third_party/webdriver \
		third_party/webrtc \
                third_party/webrtc/common_audio/third_party/fft4g \
		third_party/webrtc/common_audio/third_party/spl_sqrt_floor \
		third_party/webrtc/modules/third_party/fft \
		third_party/webrtc/modules/third_party/g711 \
		third_party/webrtc/modules/third_party/g722 \
		third_party/webrtc/rtc_base/third_party/base64 \
		third_party/webrtc/rtc_base/third_party/sigslot \
		third_party/widevine \
		third_party/woff2 \
		third_party/zlib/google \
		url/third_party/mozilla \
		v8/src/third_party/valgrind \
		v8/src/third_party/utf8-decoder \
		v8/third_party/inspector_protocol \
		v8/third_party/v8 \
                third_party/yasm \
		base/third_party/libevent \
		third_party/xdg-utils \
		third_party/yasm/run_yasm.py \
                third_party/adobe \
		third_party/speech-dispatcher \
		third_party/usb_ids \
		third_party/test_fonts \
		third_party/angle/src/common/third_party/xxhash \
		third_party/libvpx \
		third_party/libvpx/source/libvpx/third_party/x86inc \
%if !%{with re2_external}
		third_party/re2 \
%endif
%if %{with remote_desktop}
		third_party/sinonjs \
		third_party/blanketjs \
		third_party/qunit \
%endif
    		third_party/icu \
   		base/third_party/icu/ \
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
    yasm \
    fontconfig \
    opus \
    zlib


# Don't use static libstdc++
sed -i '/-static-libstdc++/d' tools/gn/build/gen.py

%if %{with system_jinja2}
rmdir third_party/jinja2 
ln -s %{python2_sitelib}/jinja2 third_party/jinja2
%endif


%if %{with system_ply}
rmdir third_party/ply
ln -s %{python2_sitelib}/ply third_party/ply
%endif


%if 0%{?fedora} >= 28 || %{with clang_bundle}
sed -i \
    -e '/"-Wno-ignored-pragma-optimize"/d' build/config/compiler/BUILD.gn

sed -i \
    -e '/"-Wno-defaulted-function-deleted"/d' build/config/compiler/BUILD.gn

%endif

# Force script incompatible with Python 3 to use /usr/bin/python2
  sed -i '1s|python$|&2|' third_party/dom_distiller_js/protoc_plugins/*.py


%build

# python2 fix
export PATH="$HOME/bin/:$PATH"

# some still call gcc/g++
%if %{with clang}
%if %{with clang_bundle}
export CC=%{_builddir}/buclang/bin/clang
export CXX=%{_builddir}/buclang/bin/clang++
%else
export CC=clang
export CXX=clang++
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
    'remove_webcore_debug_symbols=true'
    'ffmpeg_branding="Chrome"'
    'proprietary_codecs=true'
%if %{with vaapi}
    'use_vaapi=true'
%else
    'use_vaapi=false'
%endif
    'use_aura=true'
    'link_pulseaudio=true'
    'linux_use_bundled_binutils=false'
    'use_custom_libcxx=false'
    'use_lld=false'
    'use_debug_fission=false'
    'use_allocator="none"'
    'use_ozone=false'
    'optimize_webui=false'
    'enable_iterator_debugging=false'
    'use_cups=true'
    'use_gnome_keyring=false'
    'use_gio=true'
    'use_gold=false'
    'use_kerberos=true'
    'use_pulseaudio=true'
    'use_system_freetype=false'
    'use_sysroot=false'
    'enable_hangout_services_extension=true'
    'enable_widevine=true'
    'enable_nacl=false'
    'enable_swiftshader=true'
    'enable_hevc_demuxing=true'
    "google_api_key=\"AIzaSyD1hTe85_a14kr1Ks8T3Ce75rvbR1_Dx7Q\""
    "google_default_client_id=\"4139804441.apps.googleusercontent.com\""
    "google_default_client_secret=\"KDTRKEZk2jwT_7CDpcmMA--P\""
%if %{with system_ffmpeg}
    'is_component_ffmpeg=true' 
%endif
%if %{with component_build}
    'is_component_build=true'
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
    'jumbo_file_merge_limit=9'
%endif
    'concurrent_links=1'
    'remove_webcore_debug_symbols=true'
)


# Build files for Ninja #
gn gen --script-executable=/usr/bin/python2 --args="${_flags[*]}" out/Release 


# SUPER POWER!
jobs=$(grep processor /proc/cpuinfo | tail -1 | grep -o '[0-9]*')

%if %{with remote_desktop}
ninja-build -C out/Release remoting_all -j$jobs
%endif

# HERE the real build
%if %{with devel_tools}
%if %{with system_ffmpeg}
ninja-build -C out/Release third_party/widevine/cdm media/ffmpeg chrome chrome_sandbox chromedriver policy_templates -j$jobs 
%else
ninja-build -C out/Release third_party/widevine/cdm chrome chrome_sandbox chromedriver policy_templates -j$jobs 
%endif
%else
%if %{with system_ffmpeg}
ninja-build -C out/Release third_party/widevine/cdm media/ffmpeg chrome policy_templates -j$jobs 
%else
ninja-build -C out/Release third_party/widevine/cdm chrome policy_templates -j$jobs 
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
install -m 644 %{SOURCE13} %{buildroot}%{_datadir}/appdata/


# Brute Copy
cp \
    out/Release/{chrome_{100,200}_percent,resources,views_mus_resources,headless_lib}.pak \
    out/Release/{*.bin,*.so,v8_context_snapshot_generator,mksnapshot,brotli,character_data_generator,xdg-settings,xdg-mime,transport_security_state_generator} \
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
mv -f out/Release/swiftshader %{buildroot}/%{chromiumdir}/

for size in 22 24 48 64 128 256; do
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

# Add directories for policy management
mkdir -p %{buildroot}%{_sysconfdir}/chromium/policies/managed
mkdir -p %{buildroot}%{_sysconfdir}/chromium/policies/recommended

cp -a out/Release/gen/chrome/app/policy/common/html/en-US/*.html .
cp -a out/Release/gen/chrome/app/policy/linux/examples/chrome.json .

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
    %{buildroot}/%{_datadir}/drirc.d/10-chromium.conf

# Mangling fix
# bash
sed -i 's|/bin/bash|/usr/bin/bash|g' %{buildroot}/usr/lib64/chrome-remote-desktop/is-remoting-session
sed -i 's|/bin/bash|/usr/bin/bash|g' %{buildroot}/%{chromiumdir}/xdg-settings
sed -i 's|/bin/bash|/usr/bin/bash|g' %{buildroot}/%{chromiumdir}/xdg-mime
sed -i 's|/bin/bash|/usr/bin/bash|g' %{buildroot}/%{_sysconfdir}/chromium/remoting_native_messaging_host/chrome-remote-desktop-host
sed -i 's|/bin/bash|/usr/bin/bash|g' %{buildroot}/%{_sysconfdir}/chromium/remoting_native_messaging_host/user-session
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
%doc AUTHORS chrome_policy_list.html *.json
%config %{_sysconfdir}/%{name}/
%{_bindir}/%{name}
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/gnome-control-center/default-apps/%{name}.xml
%{_datadir}/icons/hicolor/16x16/apps/chromium.png
%{_datadir}/icons/hicolor/22x22/apps/chromium.png
%{_datadir}/icons/hicolor/24x24/apps/chromium.png
%{_datadir}/icons/hicolor/32x32/apps/chromium.png
%{_datadir}/icons/hicolor/48x48/apps/chromium.png
%{_datadir}/icons/hicolor/64x64/apps/chromium.png
%{_datadir}/icons/hicolor/128x128/apps/chromium.png
%{_datadir}/icons/hicolor/256x256/apps/chromium.png
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

%{chromiumdir}/natives_blob.bin
%{chromiumdir}/snapshot_blob.bin
%{chromiumdir}/*.pak
%dir %{chromiumdir}/locales
%{chromiumdir}/locales/*.pak
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
%{chromiumdir}/swiftshader/
%{chromiumdir}/transport_security_state_generator
%{chromiumdir}/v8_context_snapshot.bin
%{chromiumdir}/v8_context_snapshot_generator
%{chromiumdir}/xdg-mime
%{chromiumdir}/xdg-settings

%files libs
%{chromiumdir}/lib*.so*
%exclude %{chromiumdir}/libwidevinecdm.so
%exclude %{chromiumdir}/libwidevinecdmadapter.so
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
