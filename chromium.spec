%bcond_with normalsource

%bcond_without specific_source


%global ffmpeg 0
%global clang 1
%global libva 0
%global libvpx 0
%global icu 0
%global gtk3 1
%global libpng 1
# disable libxml to avoid not opening
#http://base.consultant.ru/cons/cgi/online.cgi?req=doc;base=LAW;n=160129;div=LAW;rnd=0.4700782325977544
%global xml 0
%global crd_path %{_libdir}/chrome-remote-desktop

%if %{defined rhel}
%global _missing_build_ids_terminate_build 0
%global debug_package %{nil}
%global chromium_system_libs 0
# build with gcc for RHEL to avoid
# http://koji.russianfedora.pro/koji/getfile?taskID=67919&name=build.log&offset=-4000
%global clang 0
%else
%global chromium_system_libs 1
%if 0%{?fedora} >= 23
%global ffmpeg 0
%endif
%if 0%{?fedora} >= 24
%global libvpx 1
%endif
%endif


Summary:	A fast webkit-based web browser
Name:		chromium
Version:	53.0.2785.143
Release:	3%{?dist}

Group:		Applications/Internet
License:	BSD, LGPL
URL:		http://www.chromium.org/

%if %{with normalsource}
Source1:	https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
%endif
# Use chromium-latest.py to generate clean tarball from released build tarballs, found here:
# http://build.chromium.org/buildbot/official/
# For Chromium Fedora use chromium-latest.py --stable --ffmpegclean --ffmpegarm
# If you want to include the ffmpeg arm sources append the --ffmpegarm switch
# https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%%{version}.tar.xz

# Also, only used if you want to reproduce the clean tarball.
Source5: https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/clean_ffmpeg.sh
Source6:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/chromium-latest.py
Source7:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/get_free_ffmpeg_source_files.py
# Get the names of all tests (gtests) for Linux
# Usage: get_linux_tests_name.py chromium-%%{version} --spec
Source8:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/get_linux_tests_names.py

Source10:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/chromium-wrapper
Source20:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/chromium-browser.desktop
Source30:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/master_preferences
Source32:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/chromium.default
Source33:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/chrome-remote-desktop.service
Source34:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/chromium-browser.appdata.xml

Source997:	https://github.com/UnitedRPMs/chromium-freeworld/raw/master/depot_tools.tar.xz
Source998:	https://github.com/UnitedRPMs/chromium-freeworld/raw/master/gn-binaries.tar.xz

Conflicts:	chromium-testing
Conflicts:	chromium-unstable

Patch0:		https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/chromium-30.0.1599.66-master-prefs-path.patch

# PATCH-FIX-UPSTREAM Add more charset aliases
Patch6:		https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/chromium-more-codec-aliases.patch
# PATCH-FIX-OPENSUSE Compile the sandbox with -fPIE settings
Patch15:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/chromium-25.0.1364.172-sandbox-pie.patch

# archlinux arm enhancement patches
Patch100:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/arm-webrtc-fix.patch
Patch101:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/chromium-arm-r0.patch

# fix https://bugs.chromium.org/p/chromium/issues/detail?id=548254
# build on EL7
Patch198:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/issue1637423004_100001.diff
# fix https://bugs.chromium.org/p/chromium/issues/detail?id=585513
# vaInitialize failed VA error: unknown libva error
Patch199:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/issue1688073002_40001.diff
# http://bazaar.launchpad.net/~saiarcot895/chromium-browser/chromium-browser.trusty.beta/revision/230#debian/patches/enable_vaapi_on_linux.diff
Patch200:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/enable_vaapi_on_linux.diff
# Google patched their bundled copy of icu 54 to include API functionality that wasn't added until 55.
# :P
Patch201:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/chromium-45.0.2454.101-system-icu-56-does-not-have-detectHostTimeZone.patch
# (cjw) fix build problem with system libvpx due to usage of private header file
# mageia patch
Patch202:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/chromium-46-svc_context.patch
# fix build with icu other than 54
Patch204:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/chromium-system-icu-r0.patch
# (cjw) Don't disable deprecated APIs in ffmpeg header files, some of which change the ABI.
#	From Gentoo: http://mirror.yandex.ru/gentoo-portage/www-client/chromium/files/chromium-system-ffmpeg-r2.patch
Patch205:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/chromium-system-ffmpeg-r3.patch
# (cjw) fix webrtc build with system ffmpeg
Patch206:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/chromium-51-system-ffmpeg-3.patch

Patch208:	https://raw.githubusercontent.com/UnitedRPMs/chromium-freeworld/master/chromium-52.0.2743.82-cups22.patch

BuildRequires:  tar
BuildRequires:  SDL-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  bison
BuildRequires:  bzip2-devel
BuildRequires:  cups-devel
BuildRequires:  desktop-file-utils
BuildRequires:  dirac-devel >= 1.0.0
BuildRequires:  elfutils-libelf-devel
BuildRequires:  elfutils-devel
BuildRequires:  expat-devel
BuildRequires:  fdupes
BuildRequires:  flac-devel
BuildRequires:  flex
BuildRequires:  freetype-devel
BuildRequires:  gperf
BuildRequires:  gsm
BuildRequires:  gsm-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  gyp
BuildRequires:  hicolor-icon-theme
BuildRequires:  hunspell-devel
BuildRequires:  imlib2-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  krb5-devel
BuildRequires:  libatomic
BuildRequires:  libcap-devel
BuildRequires:  libdc1394
BuildRequires:  libdc1394-devel
BuildRequires:  libdrm-devel
BuildRequires:  libdrm-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libgnome-keyring-devel
BuildRequires:  libogg-devel
BuildRequires:  liboil-devel >= 0.3.15
BuildRequires:  libtheora-devel >= 1.1
BuildRequires:  libusbx-devel
BuildRequires:  libvdpau-devel
BuildRequires:  libvorbis-devel
BuildRequires:	SDL-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	bison
BuildRequires:	bzip2-devel
BuildRequires:	cups-devel
BuildRequires:	desktop-file-utils
BuildRequires:	dirac-devel >= 1.0.0
BuildRequires:	elfutils-libelf-devel
BuildRequires:	elfutils-devel
BuildRequires:	expat-devel
BuildRequires:	fdupes
BuildRequires:	flac-devel
BuildRequires:	flex
BuildRequires:	freetype-devel
BuildRequires:	gperf
BuildRequires:	gsm
BuildRequires:	gsm-devel
BuildRequires:	gstreamer1-devel
BuildRequires:	gstreamer1-plugins-base-devel
BuildRequires:	gyp
BuildRequires:	hicolor-icon-theme
BuildRequires:	hunspell-devel
BuildRequires:	imlib2-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	krb5-devel
BuildRequires:	libatomic
BuildRequires:	libcap-devel
BuildRequires:	libdc1394
BuildRequires:	libdc1394-devel
BuildRequires:	libdrm-devel
BuildRequires:	libdrm-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libogg-devel
BuildRequires:	liboil-devel >= 0.3.15
BuildRequires:	libtheora-devel >= 1.1
BuildRequires:	libusbx-devel
BuildRequires:	libvdpau-devel
BuildRequires:	libvorbis-devel
%if 0%{?libvpx}
# requires patched version of libvpx with svc_context.h file
# http://github.com/RussianFedora/libvpx/commit/aad752872cc0a05f15419aa915f108ad75f6a2fe
BuildRequires:	libvpx-devel >= 1.5.0
%endif
BuildRequires:	ncurses-devel
BuildRequires:	ninja-build
BuildRequires:	pam-devel
BuildRequires:	pciutils-devel
BuildRequires:	perl(Switch)
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(cairo) >= 1.6
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
%if 0%{gtk3}
BuildRequires:	pkgconfig(gtk+-3.0)
%endif
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(nspr) >= 4.9.5
BuildRequires:	pkgconfig(nss) >= 3.14
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	schroedinger-devel
BuildRequires:	slang-devel
BuildRequires:	speech-dispatcher-devel
BuildRequires:	sqlite-devel
BuildRequires:	texinfo
BuildRequires:	util-linux
%if 0%{?ffmpeg}
BuildRequires:	ffmpeg-devel
%endif
BuildRequires:	valgrind-devel
%if 0%{?fedora}
BuildRequires:	python-jinja2
BuildRequires:	python-markupsafe
BuildRequires:	python-ply
%endif

%if 0%{?chromium_system_libs}
BuildRequires:	fontconfig-devel
%if 0%{icu}
BuildRequires:	libicu-devel >= 5.4
%endif
BuildRequires:	libjpeg-turbo-devel
BuildRequires:	perl-JSON
BuildRequires:	pkgconfig(jsoncpp)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	pkgconfig(libmtp)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(minizip)
BuildRequires:	pkgconfig(minizip)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(protobuf)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(zlib)
#BuildRequires:	re2-devel
BuildRequires:	snappy-devel
BuildRequires:	usbutils
BuildRequires:	yasm
%endif

%if ! %{defined rhel}
#BuildRequires:	lame-devel
#BuildRequires:	opencore-amr-devel
BuildRequires:	wdiff
#BuildRequires:	x264-devel
#BuildRequires:	xvidcore-devel
%endif

%if 0%{?clang}
BuildRequires:	clang
%endif

%if 0%{?libva}
BuildRequires:	libva-devel
%endif

# remote desktop needs this
BuildRequires:	pam-devel
BuildRequires:	systemd

# for /usr/bin/appstream-util
BuildRequires:	libappstream-glib

# dowload source
BuildRequires:	wget

Requires:	hicolor-icon-theme
# Missing libva in AutoRequires
Requires:	libva

Obsoletes:	chromium-pdf-plugin < 17.0.0.169
Provides:	chromium-freeworld = %{version}-%{release}

ExclusiveArch:	x86_64 i686

%description
Chromium is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

This is the stable channel Chromium browser. It offers a rock solid
browser which is updated with features and fixes once they have been
thoroughly tested. If you want the latest features, install the
chromium-browser-unstable package instead.

Note: If you are reverting from unstable to stable or beta channel, you may
experience tab crashes on startup. This crash only affects tabs restored
during the first launch due to a change in how tab state is stored.
See http://bugs.chromium.org/34688. It's always a good idea to back up
your profile before changing channels.

%package libs
Summary: Shared libraries used by chromium (and chrome-remote-desktop)
Requires: chromium-libs-media-freeworld%{_isa} = %{version}-%{release}

%description libs
Shared libraries used by chromium (and chrome-remote-desktop).

%package -n chrome-remote-desktop
Summary: Remote desktop support for google-chrome & chromium
Requires(pre):	shadow-utils
Requires(post):	systemd
Requires(preun): systemd
Requires(postun): systemd
Requires:	xorg-x11-server-Xvfb


%description -n chrome-remote-desktop
Remote desktop support for google-chrome & chromium.


%package -n chromedriver
Summary:	WebDriver for Google Chrome/Chromium
Group:		Development/Libraries
Conflicts:	chromedriver-testing
Conflicts:	chromedriver-unstable

%description -n chromedriver
WebDriver is an open source tool for automated testing of webapps across many
browsers. It provides capabilities for navigating to web pages, user input,
JavaScript execution, and more. ChromeDriver is a standalone server which
implements WebDriver's wire protocol for Chromium. It is being developed by
members of the Chromium and WebDriver teams.

%package libs-media-freeworld
Summary: Chromium media libraries built with all possible codecs
Provides: chromium-libs-media%{_isa} = %{version}-%{release}

%description libs-media-freeworld
Chromium media libraries built with all possible codecs. Chromium is an
open-source web browser, powered by WebKit (Blink). This package replaces
the default chromium-libs-media package, which is limited in what it
can include.


%prep

%if %{with normalsource}
tar xJf %{S:1} -C %{_builddir}
%else
%if %{with specific_source}
wget -c https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
%else
if [ ! -f %{_builddir}/chromium-%{version}-clean.tar.xz ]; then
python %{_sourcedir}/chromium-latest.py --stable --ffmpegclean --ffmpegarm
fi
%endif
# tar xJf %{_builddir}/chromium-%{version}-clean.tar.xz -C %{_builddir}
tar xJf %{_builddir}/chromium-%{version}.tar.xz -C %{_builddir}
%endif

%setup -q -T -c -n depot_tools -a 998
%setup -q -T -c -n tools -a 997

cd %{_builddir}/chromium-%{version}/

%if 0%{?chromium_system_libs}
# files we do not want from upstream source bundles
rm -rf breakpad/src/processor/testdata/
rm -rf chrome/app/test_data/dlls/
rm -rf chrome/common/extensions/docs/
#rm -rf chrome/test/data/
rm -rf chrome/tools/test/reference_build/chrome_linux/
rm -rf components/test/data/component_updater/jebgalgnebhfojomionfpkfelancnnkf/component1.dll
rm -rf content/test/data/
rm -rf net/data/
rm -rf ppapi/examples/
rm -rf ppapi/native_client/tests/
rm -rf third_party/apache-win32/
rm -rf third_party/binutils/
rm -rf third_party/expat/files/
%if 0%{?ffmpeg}
rm -rf third_party/ffmpeg/*/*
rm -rf third_party/ffmpeg/*.[ch]
%endif
rm -rf third_party/flac/include
rm -rf third_party/flac/src
%if 0%{icu}
rm -rf third_party/icu/android
rm -rf third_party/icu/linux
rm -rf third_party/icu/mac
rm -rf third_party/icu/patches
rm -rf third_party/icu/public
rm -rf third_party/icu/source
rm -rf third_party/icu/windows
%endif
rm -rf third_party/lcov
rm -rf third_party/libevent/*/*
rm -rf third_party/libevent/*.[ch]
%if 0%{?libvpx}
rm -rf third_party/libvpx/source/libvpx
%endif
rm -rf libexif/sources
rm -rf libjpeg/*.[ch]
rm -rf libjpeg_turbo
%if 0%{?libpng}
rm -rf libpng/*.[ch]
%endif
rm -rf libxslt/libexslt
rm -rf libxslt/libxslt
rm -rf libxslt/linux
rm -rf libxslt/mac
rm -rf libxslt/win32
rm -rf mesa/src/src
rm -rf swig
rm -rf third_party/WebKit/LayoutTests/
rm -rf third_party/WebKit/Tools/Scripts/
rm -rf third_party/xdg-utils/tests/
rm -rf third_party/yasm/source/
rm -rf tools/gyp/test/
rm -rf v8/test/
%endif

%patch0 -p1 -b .master-prefs

# openSUSE patches
%patch6 -p0
%patch15 -p1

# archlinux arm enhancements
%patch100 -p0
%patch101 -p0

%if 0%{?libva}
%patch198 -p1
%patch199 -p1
%patch200 -p1
%endif

%if 0%{icu}
%patch201 -p1 -b .system-icu
%if 0%{?fedora} >= 24
%patch204 -p0 -b .icu-ver
%endif
%endif

%if 0%{?libvpx}
%patch202 -p1 -b .system-libvpx
%endif

%if 0%{?ffmpeg}
%patch205 -p1
%patch206 -p1
%endif

%patch208 -p1

### build with widevine support

# Patch from crbug (chromium bugtracker)
# fix the missing define (if not, fail build) (need upstream fix) (https://crbug.com/473866)
sed '14i#define WIDEVINE_CDM_VERSION_STRING "Something fresh"' -i "third_party/widevine/cdm/stub/widevine_cdm_version.h"

# Hard code extra version
FILE=chrome/common/channel_info_posix.cc
sed -i.orig -e 's/getenv("CHROME_VERSION_EXTRA")/"UnitedRPMs Project"/' $FILE
cmp $FILE $FILE.orig && exit 1

%ifarch x86_64
sed -i "s#/lib/#/lib64/#g" %{SOURCE20}
%endif

%ifarch i686
sed -i "s#/lib64/#/lib/#g" %{SOURCE20}
%endif

%build
cd %{_builddir}/chromium-%{version}/
# https://groups.google.com/a/chromium.org/forum/#!topic/chromium-packagers/9JX1N2nf4PU
touch chrome/test/data/webui/i18n_process_css_test.html
touch chrome/test/data/webui_test_resources.grd

buildconfig+="-Dwerror=
		-Dlinux_sandbox_chrome_path=%{_libdir}/%{name}/chrome
		-Dproprietary_codecs=1
		-Dremove_webcore_debug_symbols=1
		-Dlogging_like_official_build=1
		-Dlinux_fpic=1
		-Ddisable_sse2=1
		-Dcomponent=shared_library
		-Ddisable_nacl=1
		-Ddisable_glibc=1
		-Ddisable_pnacl=1
		-Ddisable_newlib_untar=0
		-Duse_system_xdg_utils=1
		-Denable_hotwording=0
		-Denable_widevine=1
		-Duse_aura=1
		-Denable_hidpi=1
		-Denable_touch_ui=1
		-Denable_pepper_cdms=1
		-Denable_webrtc=1
		-Drtc_use_h264=1
		-Duse_gnome_keyring=1
		-Duse_gconf=0
		-Duse_sysroot=0"
%if 0%{gtk3}
buildconfig+=" -Duse_gtk3=1"
%else
buildconfig+=" -Dtoolkit_uses_gtk=0"
%endif

%if 0%{icu}
buildconfig+=" -Duse_system_icu=1"
%else
buildconfig+=" -Duse_system_icu=0"
%endif

%if 0%{?ffmpeg}
buildconfig+=" -Duse_system_ffmpeg=1"
%else
buildconfig+=" -Duse_system_ffmpeg=0
		-Dbuild_ffmpegsumo=1
		-Dffmpeg_branding=Chrome"
%endif

%if ! %{defined rhel}
buildconfig+=" -Dlibspeechd_h_prefix=speech-dispatcher/"
%endif

%if 0%{?clang}
buildconfig+=" -Dclang=1
		-Dclang_use_chrome_plugins=0"
%else
buildconfig+=" -Dclang=0"
%endif

%if 0%{?chromium_system_libs}
buildconfig+=" -Duse_system_flac=1
		-Duse_system_speex=1
		-Duse_system_fontconfig=1
		-Duse_system_jsoncpp=1
		-Duse_system_libexif=1
		-Duse_system_libevent=1
		-Duse_system_libmtp=1
		-Duse_system_opus=1
		-Duse_system_bzip2=1
		-Duse_system_harfbuzz=1
		-Duse_system_libjpeg=1
		-Duse_system_libxslt=1
		-Duse_system_libyuv=1
		-Duse_system_nspr=1
		-Duse_system_snappy=1
		-Duse_system_zlib=1
		-Duse_system_yasm=1"

%if 0%{?libpng}
buildconfig+=" -Duse_system_libpng=1"
%else
buildconfig+=" -Duse_system_libpng=0"
%endif

%if 0%{xml}
buildconfig+=" -Duse_system_libxml=1"
%else
buildconfig+=" -Duse_system_libxml=0"
%endif

%if 0%{?libvpx}
buildconfig+=" -Duse_system_libvpx=1"
%else
buildconfig+=" -Duse_system_libvpx=0"
%endif
# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=764911
# Segfault with system protobuf at this time
buildconfig+=" -Duse_system_protobuf=0"
%else
buildconfig+=" -Duse_system_flac=0
		-Duse_system_speex=0
		-Duse_system_libexif=0
		-Duse_system_libevent=0
		-Duse_system_libmtp=0
		-Duse_system_opus=0
		-Duse_system_bzip2=0
		-Duse_system_harfbuzz=0
		-Duse_system_libjpeg=0
		-Duse_system_libpng=0
		-Duse_system_libxslt=0
		-Duse_system_libyuv=0
		-Duse_system_sqlite=0
		-Duse_system_nspr=0
		-Duse_system_protobuf=0
		-Duse_system_yasm=0"
%endif

%ifarch x86_64
buildconfig+=" -Dsystem_libdir=lib64
		-Dtarget_arch=x64"
%endif

buildconfig+=" -Duse_pulseaudio=1
		-Dlinux_link_libpci=1
		-Dlinux_link_gnome_keyring=1
		-Dlinux_link_gsettings=1
		-Dlinux_link_libgps=1
		-Dlinux_link_libspeechd=1
		-Djavascript_engine=v8
		-Dlinux_use_gold_binary=0
		-Dlinux_use_gold_flags=0
		-Dgoogle_api_key=AIzaSyD1hTe85_a14kr1Ks8T3Ce75rvbR1_Dx7Q
		-Dgoogle_default_client_id=4139804441.apps.googleusercontent.com
		-Dgoogle_default_client_secret=KDTRKEZk2jwT_7CDpcmMA--P"

%if 0%{?clang}
export CC=/usr/bin/clang
export CXX=/usr/bin/clang++
# Modern Clang produces a *lot* of warnings
export CXXFLAGS="${CXXFLAGS} -Wno-unknown-warning-option -Wno-unused-local-typedef -Wunknown-attributes -Wno-tautological-undefined-compare"
export GYP_DEFINES="clang=1"
%endif

%if 0%{?fedora}
# Look, I don't know. This package is spit and chewing gum. Sorry.
rm -rf third_party/jinja2 third_party/markupsafe
ln -s %{python_sitelib}/jinja2 third_party/jinja2
ln -s %{python_sitearch}/markupsafe third_party/markupsafe
%endif

# Fix hardcoded path in remoting code
sed -i 's|/opt/google/chrome-remote-desktop|%{crd_path}|g' remoting/host/setup/daemon_controller_delegate_linux.cc

build/linux/unbundle/replace_gyp_files.py $buildconfig

export GYP_GENERATORS='ninja'
./build/gyp_chromium build/all.gyp --depth=. $buildconfig

mkdir -p out/Release

ninja-build -C out/Release chrome chrome_sandbox chromedriver widevinecdmadapter clearkeycdm

# remote client
pushd remoting
ninja-build -C ../out/Release -vvv remoting_me2me_host remoting_start_host remoting_it2me_native_messaging_host remoting_me2me_native_messaging_host remoting_native_messaging_manifests remoting_resources
popd

%install
cd %{_builddir}/chromium-%{version}/
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/%{name}/locales
mkdir -p %{buildroot}%{_libdir}/%{name}/themes
mkdir -p %{buildroot}%{_libdir}/%{name}/default_apps
mkdir -p %{buildroot}%{_mandir}/man1
install -m 755 %{SOURCE10} %{buildroot}%{_libdir}/%{name}/
install -m 755 out/Release/chrome %{buildroot}%{_libdir}/%{name}/
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{_libdir}/%{name}/chrome-sandbox
cp -a out/Release/chromedriver %{buildroot}%{_libdir}/%{name}/chromedriver
install -m 644 out/Release/chrome.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -m 644 out/Release/*.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/icudtl.dat %{buildroot}%{_libdir}/%{name}/

cp -a out/Release/*_blob.bin %{buildroot}%{_libdir}/%{name}/

# chromium components
mkdir -p %{buildroot}%{_libdir}/%{name}/lib/
cp -av out/Release/lib/*.so %{buildroot}%{_libdir}/%{name}/lib/

install -m 644 out/Release/locales/*.pak %{buildroot}%{_libdir}/%{name}/locales/
install -m 644 out/Release/chrome_*_percent.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/content_resources.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/resources.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 chrome/browser/resources/default_apps/* %{buildroot}%{_libdir}/%{name}/default_apps/

# install wrapper
ln -s %{_libdir}/%{name}/chromium-wrapper %{buildroot}%{_bindir}/%{name}
sed -i "s!@LIBDIR@!%{_libdir}!g" %{buildroot}%{_libdir}/%{name}/chromium-wrapper

ln -s %{_libdir}/%{name}/chromedriver %{buildroot}%{_bindir}/chromedriver

# create global config file
mkdir -p %{buildroot}%{_sysconfdir}/default
install -m644 %{SOURCE32} %{buildroot}%{_sysconfdir}/default/%{name}

# create pepper dir. talkplugin works fine only if sylinks in pepper
mkdir -p %{buildroot}%{_libdir}/%{name}/pepper

find out/Release/resources/ -name "*.d" -exec rm {} \;
cp -r out/Release/resources %{buildroot}%{_libdir}/%{name}

# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{SOURCE20} %{buildroot}%{_datadir}/applications/

install -D -m0644 %{SOURCE34} ${RPM_BUILD_ROOT}%{_datadir}/appdata/%{name}.appdata.xml
appstream-util validate-relax --nonet ${RPM_BUILD_ROOT}%{_datadir}/appdata/%{name}.appdata.xml

# icon
for i in 22 24 48 64 128 256; do
	mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
	install -m 644 chrome/app/theme/chromium/product_logo_$i.png \
		%{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

# Install the master_preferences file
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 %{SOURCE30} %{buildroot}%{_sysconfdir}/%{name}/

# Remote desktop bits
mkdir -p %{buildroot}%{crd_path}

pushd %{buildroot}%{crd_path}
ln -s %{_libdir}/%{name}/lib lib
popd

# See remoting/host/installer/linux/Makefile for logic
cp -a out/Release/native_messaging_host %{buildroot}%{crd_path}/native-messaging-host
cp -a out/Release/remote_assistance_host %{buildroot}%{crd_path}/remote-assistance-host
cp -a out/Release/remoting_locales %{buildroot}%{crd_path}/
cp -a out/Release/remoting_me2me_host %{buildroot}%{crd_path}/chrome-remote-desktop-host
cp -a out/Release/remoting_start_host %{buildroot}%{crd_path}/start-host

# chromium
mkdir -p %{buildroot}%{_sysconfdir}/chromium/native-messaging-hosts
# google-chrome
mkdir -p %{buildroot}%{_sysconfdir}/opt/chrome/
cp -a out/Release/remoting/* %{buildroot}%{_sysconfdir}/chromium/native-messaging-hosts/
for i in %{buildroot}%{_sysconfdir}/chromium/native-messaging-hosts/*.json; do
	sed -i 's|/opt/google/chrome-remote-desktop|%{crd_path}|g' $i
done
pushd %{buildroot}%{_sysconfdir}/opt/chrome/
ln -s ../../chromium/native-messaging-hosts native-messaging-hosts
popd

mkdir -p %{buildroot}/var/lib/chrome-remote-desktop
touch %{buildroot}/var/lib/chrome-remote-desktop/hashes

mkdir -p %{buildroot}%{_sysconfdir}/pam.d/
pushd %{buildroot}%{_sysconfdir}/pam.d/
ln -s system-auth chrome-remote-desktop
popd

cp -a remoting/host/linux/linux_me2me_host.py %{buildroot}%{crd_path}/chrome-remote-desktop
cp -a remoting/host/installer/linux/is-remoting-session %{buildroot}%{crd_path}/

mkdir -p %{buildroot}%{_unitdir}
cp -a %{SOURCE33} %{buildroot}%{_unitdir}/
sed -i 's|@@CRD_PATH@@|%{crd_path}|g' %{buildroot}%{_unitdir}/chrome-remote-desktop.service

# License
install -Dm644 %{_builddir}/chromium-%{version}/LICENSE %{buildroot}/usr/share/licenses/chromium/LICENSE

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

%pre -n chrome-remote-desktop
getent group chrome-remote-desktop >/dev/null || groupadd -r chrome-remote-desktop

%post -n chrome-remote-desktop
%systemd_post chrome-remote-desktop.service

%preun -n chrome-remote-desktop
%systemd_preun chrome-remote-desktop.service

%postun -n chrome-remote-desktop
%systemd_postun_with_restart chrome-remote-desktop.service

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/%{name}
%config %{_sysconfdir}/default/%{name}
%{_bindir}/%{name}
%{_libdir}/%{name}/chromium-wrapper
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/chrome-sandbox
%{_libdir}/%{name}/locales
%{_libdir}/%{name}/chrome_*_percent.pak
%{_libdir}/%{name}/content_resources.pak
%{_libdir}/%{name}/keyboard_resources.pak
%{_libdir}/%{name}/resources.pak
%{_libdir}/%{name}/icudtl.dat
%{_libdir}/%{name}/*_blob.bin
%{_libdir}/%{name}/resources
%{_libdir}/%{name}/themes
%{_libdir}/%{name}/default_apps
%dir %{_libdir}/%{name}/pepper
%{_mandir}/man1/%{name}*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/licenses/chromium/LICENSE

%files libs
%{_libdir}/%{name}/lib

%files -n chrome-remote-desktop
%{crd_path}/chrome-remote-desktop
%{crd_path}/chrome-remote-desktop-host
%{crd_path}/is-remoting-session
%{crd_path}/lib
%{crd_path}/native-messaging-host
%{crd_path}/remote-assistance-host
%{_sysconfdir}/pam.d/chrome-remote-desktop
%{_sysconfdir}/chromium/native-messaging-hosts/
%{_sysconfdir}/opt/chrome/
%{crd_path}/remoting_locales/
%{crd_path}/start-host
%{_unitdir}/chrome-remote-desktop.service
/var/lib/chrome-remote-desktop/

%files -n chromedriver
%defattr(-,root,root,-)
%{_bindir}/chromedriver
%{_libdir}/%{name}/chromedriver

%files libs-media-freeworld
%{_libdir}/%{name}/lib/libffmpeg.so*
%{_libdir}/%{name}/lib/libmedia.so*

%changelog

* Thu Oct 27 2016 David Vasquez <davidjeremias82 AT gmail DOT com>  53.0.2785.143-3
- Auto Source conditional

* Fri Sep 30 2016 David Vasquez <davidjeremias82 AT gmail DOT com>  53.0.2785.143-2
- Updated to 53.0.2785.143

* Sun Sep 18 2016 Pavlo Rudyi <paulcarroty at riseup.net> - 53.0.2785.116-1
- Update to 53.0.2785.113
- URPMS rebranding
- Fix grammar in #841

* Fri Sep 09 2016 David Vásquez <davidjeremias82 AT gmail DOT com>  53.0.2785.101-2
- Deleted epoch tag

* Tue Sep 06 2016 David Vásquez <davidjeremias82 AT gmail DOT com>  53.0.2785.101-1
- Upstream
- New changes reduces the size of source code to 12MB (thanks to python scripts from Tom Callaway)
- Updated to 53.0.2785.101

* Mon Sep  5 2016 Arkady L. Shane <ashejn@russianfedora.pro> 53.0.2785.92-1
- update to 53.0.2785.92

* Thu Sep  1 2016 Arkady L. Shane <ashejn@russianfedora.pro> 53.0.2785.89-1
- update to 53.0.2785.89

* Wed Aug  3 2016 Arkady L. Shane <ashejn@russianfedora.pro> 52.0.2743.116-1
- update to 52.0.2743.116

* Fri Jul 29 2016 Arkady L. Shane <ashejn@russianfedora.pro> 52.0.2743.82-3
- added appdata file from Fedora

* Wed Jul 27 2016 Arkady L. Shane <ashejn@russianfedora.pro> 52.0.2743.82-2
- create separate libs package
- build with chromium-remote-desktop

* Fri Jul 22 2016 Arkady L. Shane <ashejn@russianfedora.pro> 52.0.2743.82-1
- update to 52.0.2743.82
- fix build with cups 2.2

* Thu Jul 14 2016 Arkady L. Shane <ashejn@russianfedora.pro> 52.0.2743.75-1
- update to 52.0.2743.75

* Mon Jul  4 2016 Arkady L. Shane <ashejn@russianfedora.pro> 52.0.2743.60-1
- update to 52.0.2743.60

* Tue Jun 28 2016 Arkady L. Shane <ashejn@russianfedora.pro> 52.0.2743.41-1
- update to 52.0.2743.41
- build with internal ffmpeg

* Mon Jun 27 2016 Arkady L. Shane <ashejn@russianfedora.pro> 51.0.2704.106-2.R
- apply Ubuntu titlebar patch
- enable gtk3 support for Fedora >= 24

* Tue Jun 21 2016 Arkady L. Shane <ashejn@russianfedora.pro> 51.0.2704.106-1.R
- update to 51.0.2704.106

* Tue Jun 21 2016 Arkady L. Shane <ashejn@russianfedora.pro> 51.0.2704.103-2.R
- rebuilt against new ffmpeg
- drop faac depend

* Fri Jun 17 2016 Arkady L. Shane <ashejn@russianfedora.pro> 51.0.2704.103-1.R
- update to 51.0.2704.103

* Tue Jun 14 2016 Arkady L. Shane <ashejn@russianfedora.pro> 51.0.2704.84-2.R
- rebuilt against new ffmpeg

* Tue Jun  7 2016 Arkady L. Shane <ashejn@russianfedora.pro> 51.0.2704.84-1.R
- update to 51.0.2704.84

* Fri Jun  3 2016 Arkady L. Shane <ashejn@russianfedora.pro> 51.0.2704.79-1.R
- update to 51.0.2704.79

* Thu May 26 2016 Arkady L. Shane <ashejn@russianfedora.pro> 51.0.2704.63-1.R
- update to 51.0.2704.63
- fix build with new libvpx packed without svc_context.h header

* Wed May 25 2016 Arkady L. Shane <ashejn@russianfedora.pro> 51.0.2704.61-1.R
- update to 51.0.2704.61

* Wed May 25 2016 Arkady L. Shane <ashejn@russianfedora.pro> 51.0.2704.54-1.R
- update to 51.0.2704.54

* Tue May 17 2016 Arkady L. Shane <ashejn@russianfedora.pro> 50.0.2661.102-1.R
- update to 50.0.2661.102

* Thu Apr 21 2016 Arkady L. Shane <ashejn@russianfedora.pro> 50.0.2661.86-1.R
- update to 50.0.2661.86

* Tue Apr 19 2016 Arkady L. Shane <ashejn@russianfedora.pro> 50.0.2661.75-2.R
- build fixes for webrtc code with system ffmpeg
- build with system ffmpeg for Fedora >= 23

* Thu Apr 14 2016 Arkady L. Shane <ashejn@russianfedora.pro> 50.0.2661.75-1.R
- update to 50.0.2661.75
- disable gtk3 for Fedora 24
- disable system ffmpeg

* Sun Apr 10 2016 Arkady L. Shane <ashejn@russianfedora.pro> 50.0.2661.66-1.R
- update to 50.0.2661.66
- apply patch to fix build on el7
  https://bugs.chromium.org/p/chromium/issues/detail?id=548254

* Fri Apr  1 2016 Arkady L. Shane <ashejn@russianfedora.pro> 50.0.2661.57-1.R
- update to 50.0.2661.57
- drop gtk patch
- build with gcc
- build with internal ffmpeg

* Wed Mar 30 2016 Arkady L. Shane <ashejn@russianfedora.pro> 49.0.2623.110-1.R
- update to 49.0.2623.110

* Fri Mar 25 2016 Arkady L. Shane <ashejn@russianfedora.pro> 49.0.2623.108-1.R
- update to 49.0.2623.108

* Wed Mar  9 2016 Arkady L. Shane <ashejn@russianfedora.pro> 49.0.2623.87-1.R
- update to 49.0.2623.87
- build with gcc for RHEL

* Mon Mar  7 2016 Arkady L. Shane <ashejn@russianfedora.pro> 49.0.2623.75-4.R
- chromium crashes if built with gcc 6.0. Rebuilt with clang for F24/Rawhide
  first of all. And for other distributions too.

* Fri Mar  4 2016 Arkady L. Shane <ashejn@russianfedora.pro> 49.0.2623.75-3.R
- disable vaapi

* Thu Mar  3 2016 Arkady L. Shane <ashejn@russianfedora.pro> 49.0.2623.75-2.R
- stop experiments. Build with gcc
- build with internal libxml to avoid not opening page in base.consultant.ru

* Thu Mar  3 2016 Arkady L. Shane <ashejn@russianfedora.pro> 49.0.2623.75-1.R
- update to 49.0.2623.75
- drop upstream patch
- disable pdf support as it obsolete
- enable vaapi

* Wed Mar  2 2016 Arkady L. Shane <ashejn@russianfedora.pro> 49.0.2623.64-1.R
- update to 49.0.2623.64
- enable gtk3 support
- disable re2 support
- update VAAPI and FFmpeg patches
- disable system icu

* Tue Mar  1 2016 Arkady L. Shane <ashejn@russianfedora.pro> 48.0.2564.116-4.R
- disable vaapi support as it crashes on NVIDIA cards
- build with pdf support

* Tue Feb 23 2016 Arkady L. Shane <ashejn@russianfedora.pro> 48.0.2564.116-3.R
- update vaapi patch from
  http://bazaar.launchpad.net/~saiarcot895/chromium-browser/chromium-browser.trusty.beta/revision/230#debian/patches/enable_vaapi_on_linux.diff

* Mon Feb 22 2016 Arkady L. Shane <ashejn@russianfedora.pro> 48.0.2564.116-2.R
- fix https://bugs.chromium.org/p/chromium/issues/detail?id=585513
  vaInitialize failed VA error: unknown libva error

* Fri Feb 19 2016 Arkady L. Shane <ashejn@russianfedora.pro> 48.0.2564.116-1.R
- update to 48.0.2564.116
- drop llvm-libs BR
- apply patch from upstream to build skia with gcc 6.0
- build with gcc for Rawhide

* Wed Feb 10 2016 Arkady L. Shane <ashejn@russianfedora.pro> 48.0.2564.109-1.R
- update to 48.0.2564.109

* Sun Feb  7 2016 Arkady L. Shane <ashejn@russianfedora.pro> 48.0.2564.103-1.R
- update to 48.0.2564.103

* Thu Feb  4 2016 Arkady L. Shane <ashejn@russianfedora.pro> 48.0.2564.97-2.R
- rebuilt with system ffmpeg

* Thu Jan 28 2016 Arkady L. Shane <ashejn@russianfedora.pro> 48.0.2564.97-1.R
- update to 48.0.2564.97

* Sat Jan 23 2016 Arkady L. Shane <ashejn@russianfedora.pro> 48.0.2564.82-3.R
- build chromium with clang

* Thu Jan 21 2016 Arkady L. Shane <ashejn@russianfedora.pro> 48.0.2564.82-2.R
- fix build with system vpx. Requires patched libvpx
  https://github.com/RussianFedora/libvpx/commit/aad752872cc0a05f15419aa915f108ad75f6a2fe

* Thu Jan 21 2016 Arkady L. Shane <ashejn@russianfedora.pro> 48.0.2564.82-1.R
- update to 48.0.2564.82
- fix build with icu other than 54

* Tue Jan 19 2016 Arkady L. Shane <ashejn@russianfedora.pro> 47.0.2526.111-3.R
- create subpackage with libffmpeg library

* Fri Jan 15 2016 Arkady L. Shane <ashejn@russianfedora.pro> 47.0.2526.111-2.R
- build with system libxpv for Fedora >= 24
- build with system icu for Fedora >= 24
- build with system protobuf

* Thu Jan 14 2016 Arkady L. Shane <ashejn@russianfedora.pro> 47.0.2526.111-1.R
- update to 47.0.2526.111

* Sat Jan  2 2016 Arkady L. Shane <ashejn@russianfedora.pro> 47.0.2526.106-2.R
- build with system libraries
- EL builds with internal libraries

* Wed Dec 16 2015 Arkady L. Shane <ashejn@russianfedora.pro> 47.0.2526.106-1.R
- update to 47.0.2526.106

* Thu Dec 10 2015 Arkady L. Shane <ashejn@russianfedora.pro> 47.0.2526.80-1.R
- update to 47.0.2526.80

* Wed Dec  2 2015 Arkady L. Shane <ashejn@russianfedora.pro> 47.0.2526.73-1.R
- update to 47.0.2526.73
- drop DragEvent patch

* Wed Nov 25 2015 Arkady L. Shane <ashejn@russianfedora.pro> 46.0.2490.86-3.R
- drop nss and ssl options

* Sat Nov 21 2015 Arkady L. Shane <ashejn@russianfedora.pro> 46.0.2490.86-2.R
- rebuilt with internal nss

* Wed Nov 11 2015 Arkady L. Shane <ashejn@russianfedora.pro> 46.0.2490.86-1.R
- update to 46.0.2490.86

* Sun Oct 25 2015 Arkady L. Shane <ashejn@russianfedora.pro> 46.0.2490.80-1.R
- update to 46.0.2490.80

* Wed Oct 21 2015 Arkady L. Shane <ashejn@russianfedora.pro> 46.0.2490.71-1.R
- update to 46.0.2490.71

* Thu Sep 24 2015 Arkady L. Shane <ashejn@russianfedora.pro> 45.0.2454.99-1.R
- update to 45.0.2454.99
- use gcc for Fedora 23 and later as chromium does bot build with new llvm

* Sat Sep 19 2015 Arkady L. Shane <ashejn@russianfedora.pro> 45.0.2454.93-1.R
- update to 45.0.2454.93

* Wed Sep  2 2015 Arkady L. Shane <ashejn@russianfedora.pro> 45.0.2454.85-1.R
- update to 45.0.2454.85

* Wed Aug 12 2015 Arkady L. Shane <ashejn@russianfedora.pro> 44.0.2403.155-1.R
- update to 44.0.2403.155

* Tue Aug 11 2015 Arkady L. Shane <ashejn@russianfedora.pro> 44.0.2403.130-2.R
- drop BR: chromium-widevinecdm-plugin
- change homepage to http://start.fedoraproject.org
- added -Denable_hidpi=1 and -Denable_touch_ui=1

* Tue Aug 11 2015 Arkady L. Shane <ashejn@russianfedora.pro> 44.0.2403.130-1.R
- update to 44.0.2403.130

* Wed Jul 29 2015 Arkady L. Shane <ashejn@russianfedora.pro> 44.0.2403.125-1.R
- update to 44.0.2403.125
- drop nonfree widevinecdm require

* Tue Jul 28 2015 Arkady L. Shane <ashejn@russianfedora.pro> 44.0.2403.107-1.R
- update to 44.0.2403.107

* Wed Jul 22 2015 Arkady L. Shane <ashejn@russianfedora.pro> 44.0.2403.89-1.R
- update to 44.0.2403.89

* Wed Jul 15 2015 Arkady L. Shane <ashejn@russianfedora.pro> 43.0.2357.134-1.R
- update to 43.0.2357.134

* Sat Jul 11 2015 Arkady L. Shane <ashejn@russianfedora.pro> 43.0.2357.132-1.R
- update to 43.0.2357.132

* Fri Jul  3 2015 Arkady L. Shane <ashejn@russianfedora.pro> 43.0.2357.130-1.R
- update to 43.0.2357.130

* Sun Jun 14 2015 Arkady L. Shane <ashejn@russianfedora.pro> 43.0.2357.125-1.R
- update to 43.0.2357.125

* Mon May 25 2015 Arkady L. Shane <ashejn@russianfedora.pro> 43.0.2357.85-1.R
- update to 43.0.2357.85

* Fri May 22 2015 Arkady L. Shane <ashejn@russianfedora.pro> 43.0.2357.65-1.R
- update to 43.0.2357.65

* Thu May 14 2015 Arkady L. Shane <ashejn@russianfedora.pro> 42.0.2311.153-1.R
- update to 42.0.2311.153

* Thu Apr 30 2015 Arkady L. Shane <ashejn@russianfedora.pro> 42.0.2311.135-1.R
- update to 42.0.2311.135

* Wed Apr 15 2015 Arkady L. Shane <ashejn@russianfedora.pro> 42.0.2311.90-2.R
- added O: chromium-pdf-plugin < 17.0.0.169

* Wed Apr 15 2015 Arkady L. Shane <ashejn@russianfedora.pro> 42.0.2311.90-1.R
- update to 42.0.2311.90

* Fri Apr  3 2015 Arkady L. Shane <ashejn@russianfedora.pro> 41.0.2272.118-1.R
- update to 41.0.2272.118
- fix CVE-2015-1233

* Mon Mar 23 2015 Arkady L. Shane <ashejn@russianfedora.pro> 41.0.2272.101-1.R
- update to 41.0.2272.101

* Thu Mar 12 2015 Arkady L. Shane <ashejn@russianfedora.pro> 41.0.2272.89-1.R
- update to 41.0.2272.89

* Thu Mar 12 2015 Arkady L. Shane <ashejn@russianfedora.pro> 41.0.2272.76-2.R
- disable system xml

* Thu Mar  5 2015 Arkady L. Shane <ashejn@russianfedora.pro> 41.0.2272.76-1.R
- update to 41.0.2272.76

* Thu Feb 26 2015 Arkady L. Shane <ashejn@russianfedora.pro> 40.0.2214.115-4.R
- build with clang for fedora older then 20

* Tue Feb 24 2015 Arkady L. Shane <ashejn@russianfedora.pro> 40.0.2214.115-3.R
- write widevine plugin version into header

* Mon Feb 23 2015 Arkady L. Shane <arkady.shane@rosalab.ru> 40.0.2214.115-2.R
- support widevine

* Sun Feb 22 2015 Arkady L. Shane <arkady.shane@rosalab.ru> 40.0.2214.115-1.R
- update to 40.0.2214.115

* Tue Feb 10 2015 Arkady L. Shane <arkady.shane@rosalab.ru> 40.0.2214.111-2.R
- rebuilt with internal icu

* Mon Feb  9 2015 Arkady L. Shane <arkady.shane@rosalab.ru> 40.0.2214.111-1.R
- update to 40.0.2214.111

* Mon Feb  9 2015 Arkady L. Shane <arkady.shane@rosalab.ru> 40.0.2214.94-1.R
- update to 40.0.2214.94
- update depends and build parameters
- fix crash with google hangouts
- fix webrtc calls (rf#1418)

* Thu Jan 22 2015 Arkady L. Shane <arkady.shane@rosalab.ru> 40.0.2214.91-1.R
- update to 40.0.2214.91

* Tue Jan 20 2015 Arkady L. Shane <arkady.shane@rosalab.ru> 39.0.2171.99-1.R
- update to 39.0.2171.99

* Mon Dec 29 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 39.0.2171.95-1.R
- update to 39.0.2171.95

* Mon Dec  1 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 39.0.2171.71-1.R
- update to 39.0.2171.71

* Wed Nov 19 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 39.0.2171.65-1.R
- update to 39.0.2171.65
- drop issue566583002 patch

* Mon Nov 17 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 38.0.2125.122-1.R
- update to 38.0.2125.122

* Wed Oct 08 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 38.0.2125.101-1.R
- update to 38.0.2125.101
- drop gcc 4.9 patch

* Tue Sep 16 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 37.0.2062.120-1.R
- update to 37.0.2062.120
- fix crash on 32bit gcc 4.9 builds
  https://code.google.com/p/chromium/issues/detail?id=412967

* Wed Aug 27 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 37.0.2062.94-1.R
- update to 37.0.2062.94

* Thu Aug 14 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 36.0.1985.143-1.R
- update to 36.0.1985.143

* Thu Jul 17 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 36.0.1985.125-1.R
- update to 36.0.1985.125

* Mon Jun 23 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 35.0.1916.153-2.R
- build with internal xml, xslt

* Wed Jun 11 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 35.0.1916.153-1.R
- update to 35.0.1916.153

* Wed May 21 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 35.0.1916.114-1.R
- update to 35.0.1916.114

* Fri May 16 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 34.0.1847.137-1.R
- update to 34.0.1847.137
- enable fullscreen-within-tab by default

* Fri Apr 25 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 34.0.1847.132-1.R
- update to 34.0.1847.132

* Wed Apr 23 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 34.0.1847.116-6.R
- build with ninja
- use new run wapper and default file

* Tue Apr 22 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 34.0.1847.116-5.R
- rebuilt

* Tue Apr 22 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 34.0.1847.116-4.R
- disable system protobuf. It crashes browser

* Tue Apr 15 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 34.0.1847.116-3.R
- build with enabled aura

* Thu Apr 10 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 34.0.1847.116-2.R
- install icudtl.dat to avoid segfault
- clean up spec

* Tue Apr  8 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 34.0.1847.116-1.R
- update to 34.0.1847.116

* Wed Mar  5 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 33.0.1750.146-1.R
- update to 32.0.1750.146

* Mon Feb 24 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 33.0.1750.117-1.R
- update to 32.0.1750.117

* Thu Feb 20 2014 Arkady L. Shane <arkady.shane@rosalab.ru> 33.0.1750.115-1.R
- update to 32.0.1750.115

* Wed Feb 19 2014 Arkady L. Shane <ashejn@russianfedora.ru> - 32.0.1700.107-1.R
- update to 32.0.1700.107

* Wed Jan 29 2014 Arkady L. Shane <ashejn@russianfedora.ru> - 32.0.1700.102-1.R
- update to 32.0.1700.102

* Wed Jan 15 2014 Arkady L. Shane <ashejn@russianfedora.ru> - 32.0.1700.76-1.R
- update to 32.0.1700.76

* Thu Dec  5 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 31.0.1650.63-1.R
- update to 31.0.1650.63

* Thu Nov 14 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 31.0.1650.48-1.R
- update to 31.0.1650.48

* Thu Oct 31 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 30.0.1599.114-1.R
- update to 30.0.1599.114

* Wed Sep  4 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 29.0.1547.65-1.R
- update to 29.0.1547.65

* Mon Sep  2 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 29.0.1547.62-1.R
- update to 29.0.1547.62

* Thu Aug 22 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 29.0.1547.57-1.R
- update to 29.0.1547.57

* Wed Jul 31 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 28.0.1500.95-1.R
- update to 28.0.1500.95

* Wed Jul 10 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 28.0.1500.71-1.R
- update to 28.0.1500.71

* Fri Jun 21 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 28.0.1500.52-1.R
- update to 28.0.1500.52

* Wed Jun 19 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 28.0.1500.45-1.R
- update to 28.0.1500.45

* Sat Jun  8 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 27.0.1453.110-1.R
- update to 27.0.1453.110

* Thu May 23 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 27.0.1453.93-1.R
- update to 27.0.1453.93
- drop old glibc patch
- update master pref patch
- added BR: perl-Text-ParseWords for fedora >= 19

* Tue Apr 23 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 26.0.1410.63-2.R
- new harfbuzz still broken. Build with internal

* Mon Apr 22 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 26.0.1410.63-1.R
- update to 26.0.1410.63

* Wed Apr 17 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 26.0.1410.46-2.R
- fix crash (https://bugs.webkit.org/show_bug.cgi?id=110145)

* Wed Mar 27 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 26.0.1410.46-1.R
- update to 26.0.1410.46

* Mon Mar 25 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 25.0.1364.172-3.R
- apply many openSUSE patches and fixed webm/html5 playing (in youtube)
- build with internal zlib
- build with system libbz2
- do no use system v8 and ffmpeg options defined

* Fri Mar 22 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 25.0.1364.172-2.R
- do not build proprietary codecs as they break webm
- added BR: libusbx-devel and drop libusb-devel

* Tue Mar 19 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 25.0.1364.172-1.R
- update to 25.0.1364.172

* Mon Mar 11 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 25.0.1364.160-1.R
- update to 25.0.1364.160

* Sat Feb 23 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 25.0.1364.97-3.R
- rebuilt with internal png and system jpeg
- fix "Uncaught exception" in 2 calls to webkitTransform
- fix "Unable to set period time" alsa error, taken from chromiumOS

* Sat Feb 23 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 25.0.1364.97-2.R
- rebuilt with internal jpeg

* Fri Feb 22 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 25.0.1364.97-1.R
- update to 25.0.1364.97
- enable many new build options

* Tue Feb  5 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 24.0.1312.68-1.R
- update to 24.0.1312.68

* Wed Jan 23 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 24.0.1312.56-1.R
- update to 24.0.1312.56

* Fri Jan 11 2013 Arkady L. Shane <ashejn@russianfedora.ru> - 24.0.1312.52-1.R
- update to 24.0.1312.52

* Fri Dec 21 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 23.0.1271.97-4.R
- added epoch to requires for chromedriver

* Mon Dec 17 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 23.0.1271.97-3.R
- create separate package for chromedriver

* Thu Dec 13 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 23.0.1271.97-2.R
- rebuild with ChromeDriver

* Wed Dec 12 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 23.0.1271.97-1.R
- update to 23.0.1271.97

* Sun Dec  2 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 23.0.1271.95-1.R
- update to 23.0.1271.95

* Tue Nov 27 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 23.0.1271.91-1.R
- update to 23.0.1271.91

* Wed Nov  7 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 23.0.1271.64-1.R
- update to 23.0.1271.64

* Mon Oct 22 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 22.0.1229.92-2.R
- build with internal libxml

* Tue Oct  9 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 22.0.1229.92-1.R
- update to 22.0.1229.92

* Thu Sep 27 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 22.0.1229.79-2.R
- pack new resource files

* Wed Sep 26 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 22.0.1229.79-1.R
- update to 22.0.1229.79
- turn off system zlib
  (http://code.google.com/p/chromium/issues/detail?id=143623)

* Thu Sep 20 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 21.0.1180.89-1.R
- update to 21.0.1180.89

* Thu Aug  9 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 21.0.1180.75-1.R
- update to 21.0.1180.75

* Wed Aug  1 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 21.0.1180.57-1.R
- update to 21.0.1180.57
- drop old patches

* Thu Jul 12 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 20.0.1132.57-1.R
- update to last stable 20.0.11.32.57

* Wed Jul 11 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 20.0.1132.47-3.R
- added O: chromium-ffmpeg

* Tue Jul 10 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 20.0.1132.47-2.R
- fix trouble with glibe 2.16 (is136023)
  http://code.google.com/p/chromium/issues/detail?id=136023

* Mon Jul  9 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 20.0.1132.47-1.R
- apply patch for getting bookmarks and preferences
- patch for gcc47
- many new build requires
- apply sqlite memory leak patch

* Sat Jun 30 2012 Andrew Wyatt <andrew@fuduntu.org> - 20.0.1132.47-1
- New upstream stable release

* Thu Jun 28 2012 Andrew Wyatt <andrew@fuduntu.org> - 20.0.1132.43-2
- New upstream stable release

* Sat Jun 09 2012 Andrew Wyatt <andrew@fuduntu.org> - 19.0.1084.56-1
- New upstream stable release

* Sun Jun 03 2012 Andrew Wyatt <andrew@fuduntu.org> - 19.0.1084.53-1
- New upstream stable release

* Tue May 15 2012 Andrew Wyatt <andrew@fuduntu.org> - 19.0.1084.47-1
- New upstream stable release (Chrome 19)
- Drop patch	chromium-16.0.912.32-include-glib.patch
		chromium-17.0.963.12-remove-inline.patch

* Sat May 12 2012 Andrew Wyatt <andrew@fuduntu.org> - 18.0.1025.168-1
- New upstream stable release

* Fri Apr 20 2012 Andrew Wyatt <andrew@fuduntu.org> - 18.0.1025.165-1
- New upstream stable release

* Wed Mar 07 2012 Andrew Wyatt <andrew@fuduntu.org> - 17.0.963.65-1
- Built for Fuduntu

* Tue Mar 06 2012 Claudio Matsuoka <claudio@mandriva.com> 17.0.963.65-1mdv2010.1
+ Revision: 782481
- new upstream release 17.0.963.65 (124686)
- move chromium 17 from beta to stable

* Thu Jan 26 2012 Claudio Matsuoka <claudio@mandriva.com> 16.0.912.77-1
+ Revision: 769167
- fix required package names
- new upstream release 16.0.912.77 (118311)
  * [106484] High CVE-2011-3924: Use-after-free in DOM selections
  * [107182] Critical CVE-2011-3925: Use-after-free in Safe Browsing navigation
  * [108461] High CVE-2011-3928: Use-after-free in DOM handling
  * [108605] High CVE-2011-3927: Uninitialized value in Skia
  * [109556] High CVE-2011-3926: Heap-buffer-overflow in tree builder

* Fri Jan 06 2012 Claudio Matsuoka <claudio@mandriva.com> 16.0.912.75-1
+ Revision: 758280
- new upstream release 16.0.912.75 (116452)
  * [106672] High CVE-2011-3921: Use-after-free in animation frames.
  * [107128] High CVE-2011-3919: Heap-buffer-overflow in libxml.
  * [108006] High CVE-2011-3922: Stack-buffer-overflow in glyph handling.
- detailed changelog: http://goo.gl/n2A6J

* Wed Dec 14 2011 Claudio Matsuoka <claudio@mandriva.com> 16.0.912.63-1
+ Revision: 741173
- fix libxt-devel package name in requires
- fix cups-devel package name in requires
- new upstream release 16.0.912.63 (113337)
- security fixes
  * [81753] Medium CVE-2011-3903: Out-of-bounds read in regex matching.
  * [95465] Low CVE-2011-3905: Out-of-bounds reads in libxml.
  * [98809] Medium CVE-2011-3906: Out-of-bounds read in PDF parser.
  * [99016] High CVE-2011-3907: URL bar spoofing with view-source.
  * [100863] Low CVE-2011-3908: Out-of-bounds read in SVG parsing.
  * [101010] Medium CVE-2011-3909: [64-bit only] Memory corruption in CSS
    property array.
  * [101494] Medium CVE-2011-3910: Out-of-bounds read in YUV video frame
    handling.
  * [101779] Medium CVE-2011-3911: Out-of-bounds read in PDF.
  * [102359] High CVE-2011-3912: Use-after-free in SVG filters.
  * [103921] High CVE-2011-3913: Use-after-free in Range handling.
  * [104011] High CVE-2011-3914: Out-of-bounds write in v8 i18n handling.
  * [104529] High CVE-2011-3915: Buffer overflow in PDF font handling.
  * [104959] Medium CVE-2011-3916: Out-of-bounds reads in PDF cross references.
  * [105162] Medium CVE-2011-3917: Stack-buffer-overflow in FileWatcher.
  * [107258] High CVE-2011-3904: Use-after-free in bidi handling.
- move chromium 16 to stable
- fix elfutils-devel package name in requires

* Sat Nov 12 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.120-1
+ Revision: 730285
- only include glib.h directly

* Wed Oct 26 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.106-1
+ Revision: 707420
- new upstream release 15.0.874.106 (107270)
  * fixes login issues to Barrons Online and The Wall Street Journal

* Tue Oct 25 2011 Claudio Matsuoka <claudio@mandriva.com> 15.0.874.102-1
+ Revision: 707191
- new upstream release 15.0.874.102 (106587)
  * [86758] High CVE-2011-2845: URL bar spoof in history handling.
  * [88949] Medium CVE-2011-3875: URL bar spoof with drag+drop of URLs.
  * [90217] Low CVE-2011-3876: Avoid stripping whitespace at the end of
    download filenames.
  * [91218] Low CVE-2011-3877: XSS in appcache internals page.
  * [94487] Medium CVE-2011-3878: Race condition in worker process
    initialization.
  * [95374] Low CVE-2011-3879: Avoid redirect to chrome scheme URIs.
  * [95992] Low CVE-2011-3880: Don't permit as a HTTP header delimiter.
  * [96047][96885][98053][99512][99750] High CVE-2011-3881: Cross-origin
    policy violations.
  * [96292] High CVE-2011-3882: Use-after-free in media buffer handling.
  * [96902] High CVE-2011-3883: Use-after-free in counter handling.
  * [97148] High CVE-2011-3884: Timing issues in DOM traversal.
  * [97599][98064][98556][99294][99880][100059] High CVE-2011-3885: Stale
    style bugs leading to use-after-free.
  * [98773][99167] High CVE-2011-3886: Out of bounds writes in v8.
  * [98407] Medium CVE-2011-3887: Cookie theft with javascript URIs.
  * [99138] High CVE-2011-3888: Use-after-free with plug-in and editing.
  * [99211] High CVE-2011-3889: Heap overflow in Web Audio.
  * [99553] High CVE-2011-3890: Use-after-free in video source handling.
  * [100332] High CVE-2011-3891: Exposure of internal v8 functions.
- move Chromium 15 from beta to stable
- remove Chromium 14
- add support to armv7l
- new upstream release 14.0.835.202 (103287)
- security fixes:
  * [93788] High CVE-2011-2876: Use-after-free in text line box handling
  * [95072] High CVE-2011-2877: Stale font in SVG text handling
  * [95671] High CVE-2011-2878: Inappropriate cross-origin access to the
    window prototype
  * [96150] High CVE-2011-2879: Lifetime and threading issues in audio node
    handling
  * [97451] [97520] [97615] High CVE-2011-2880: Use-after-free in the v8
    bindings
  * [97784] High CVE-2011-2881: Memory corruption with v8 hidden objects
  * [98089] Critical CVE-2011-3873: Memory corruption in shader translator
- detailed changelog at http://goo.gl/4dBM1
- new upstream release 14.0.835.186 (101821)

* Sat Sep 17 2011 Claudio Matsuoka <claudio@mandriva.com> 14.0.835.163-1
+ Revision: 700172
- new upstream release 14.0.835.163 (101024)
- security fixes:
  * [49377] High CVE-2011-2835: Race condition in the certificate cache
  * [57908] Low CVE-2011-2837: Use PIC / pie compiler flags
  * [75070] Low CVE-2011-2838: Treat MIME type more authoritatively when
    loading plug-ins
  * [76771] High CVE-2011-2839: Crash in v8 script object wrappers
  * [78427] [83031] Low CVE-2011-2840: Possible URL bar spoofs with unusual
    user interaction
  * [78639] High CVE-2011-2841: Garbage collection error in PDF
  * [82438] Medium CVE-2011-2843: Out-of-bounds read with media buffers
  * [85041] Medium CVE-2011-2844: Out-of-bounds read with mp3 files
  * [$1000] [89219] High CVE-2011-2846: Use-after-free in unload event handling
  * [$1000] [89330] High CVE-2011-2847: Use-after-free in document loader
  * [89564] Medium CVE-2011-2848: URL bar spoof with forward button
  * [89795] Low CVE-2011-2849: Browser NULL pointer crash with WebSockets
  * [89991] Medium CVE-2011-3234: Out-of-bounds read in box handling
  * [90134] Medium CVE-2011-2850: Out-of-bounds read with Khmer characters
  * [90173] Medium CVE-2011-2851: Out-of-bounds read in video handling
  * [91120] High CVE-2011-2852: Off-by-one in v8
  * [91197] High CVE-2011-2853: Use-after-free in plug-in handling
  * [92651] [94800] High CVE-2011-2854: Use-after-free in ruby / table style
    handing
  * [92959] High CVE-2011-2855: Stale node in stylesheet handling
  * [93416] High CVE-2011-2856: Cross-origin bypass in v8
  * [93420] High CVE-2011-2857: Use-after-free in focus controller
  * [93472] High CVE-2011-2834: Double free in libxml XPath handling
  * [93497] Medium CVE-2011-2859: Incorrect permissions assigned to
    non-gallery pages
  * [93587] High CVE-2011-2860: Use-after-free in table style handling
  * [93596] Medium CVE-2011-2861: Bad string read in PDF
  * [93906] High CVE-2011-2862: Unintended access to v8 built-in objects
  * [95563] Medium CVE-2011-2864: Out-of-bounds read with Tibetan characters
  * [95625] Medium CVE-2011-2858: Out-of-bounds read with triangle arrays
  * [95917] Low CVE-2011-2874: Failure to pin a self-signed cert for a session
  * [95920] High CVE-2011-2875: Type confusion in v8 object sealing
- detailed changelog at http://goo.gl/6B1kT
- copy release 14.0.835.163 from beta to stable

* Sun Sep 04 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.782.220-1
+ Revision: 698257
- new upstream release 13.0.782.220 (99552)
  * revoking trust for SSL certificates issued by DigiNotar-controlled
    intermediate CAs used by the Dutch PKIoverheid program

* Tue Aug 23 2011 Claudio Matsuoka <claudio@mandriva.com> 13.0.782.215-1
+ Revision: 696339
- add fix for tcmalloc build in cooker
- new upstream release 13.0.782.215 (97094)
- security fixes:
  * [82552] High CVE-2011-2823: Use-after-free in line box handling
  * [88216] High CVE-2011-2824: Use-after-free with counter nodes
  * [88670] High CVE-2011-2825: Use-after-free with custom fonts
  * [89402] High CVE-2011-2821: Double free in libxml XPath handling
  * [87453] High CVE-2011-2826: Cross-origin violation with empty origins
  * [90668] High CVE-2011-2827: Use-after-free in text searching
  * [91517] High CVE-2011-2828: Out-of-bounds write in v8
  * [32-bit only] [91598] High CVE-2011-2829: Integer overflow in uniform
    arrays
- detailed changelog at http://goo.gl/Lzn1m
- new upstream release 13.0.782.112 (95650)
- move release 13.0.782.107 (94237) from beta to stable
- security fixes:
  * [78841] High CVE-2011-2359: Stale pointer due to bad line box tracking
    in rendering.
  * [79266] Low CVE-2011-2360: Potential bypass of dangerous file prompt.
  * [79426] Low CVE-2011-2361: Improve designation of strings in the basic
    auth dialog.
  * [81307] Medium CVE-2011-2782: File permissions error with drag and drop.
  * [83273] Medium CVE-2011-2783: Always confirm a developer mode NPAPI
    extension install via a browser dialog.
  * [83841] Low CVE-2011-2784: Local file path disclosure via GL program log.
  * [84402] Low CVE-2011-2785: Sanitize the homepage URL in extensions.
  * [84600] Low CVE-2011-2786: Make sure the speech input bubble is always
    on-screen.
  * [84805] Medium CVE-2011-2787: Browser crash due to GPU lock re-entrancy
    issue.
  * [85559] Low CVE-2011-2788: Buffer overflow in inspector serialization.
  * [85808] Medium CVE-2011-2789: Use after free in Pepper plug-in
    instantiation.
  * [86502] High CVE-2011-2790: Use-after-free with floating styles.
  * [86900] High CVE-2011-2791: Out-of-bounds write in ICU.
  * [87148] High CVE-2011-2792: Use-after-free with float removal.
  * [87227] High CVE-2011-2793: Use-after-free in media selectors.
  * [87298] Medium CVE-2011-2794: Out-of-bounds read in text iteration.
  * [87339] Medium CVE-2011-2795: Cross-frame function leak.
  * [87548] High CVE-2011-2796: Use-after-free in Skia.
  * [87729] High CVE-2011-2797: Use-after-free in resource caching.
  * [87815] Low CVE-2011-2798: Prevent a couple of internal schemes from
    being web accessible.
  * [87925] High CVE-2011-2799: Use-after-free in HTML range handling.
  * [88337] Medium CVE-2011-2800: Leak of client-side redirect target.
  * [88591] High CVE-2011-2802: v8 crash with const lookups.
  * [88827] Medium CVE-2011-2803: Out-of-bounds read in Skia paths.
  * [88846] High CVE-2011-2801: Use-after-free in frame loader.
  * [88889] High CVE-2011-2818: Use-after-free in display box rendering.
  * [89142] High CVE-2011-2804: PDF crash with nested functions.
  * [89520] High CVE-2011-2805: Cross-origin script injection.
  * [90222] High CVE-2011-2819: Cross-origin violation in base URI handling.
- detailed changelog at http://goo.gl/25VH4

* Fri Jul 29 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.124-1
+ Revision: 692282
- new upstream release 112-12.0.742.124 (92024)

* Tue Jun 28 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.112-1
+ Revision: 687931
- new upstream release 12.0.742.112 (90785)
- security fixes:
  * [77493] Medium CVE-2011-2345: Out-of-bounds read in NPAPI string handling.
  * [84355] High CVE-2011-2346: Use-after-free in SVG font handling.
  * [85003] High CVE-2011-2347: Memory corruption in CSS parsing.
  * [85102] High CVE-2011-2350: Lifetime and re-entrancy issues in the HTML
    parser.
  * [85177] High CVE-2011-2348: Bad bounds check in v8.
  * [85211] High CVE-2011-2351: Use-after-free with SVG use element.
  * [85418] High CVE-2011-2349: Use-after-free in text selection.
- detailed changelog at http://goo.gl/PPBY4

* Tue Jun 07 2011 Claudio Matsuoka <claudio@mandriva.com> 12.0.742.91-1
+ Revision: 683117
- new upstream release 12.0.742.91 (stable)
  * Hardware accelerated 3D CSS
  * New Safe Browsing protection against downloading malicious files
  * Ability to delete Flash cookies from inside Chrome
  * Launch Apps by name from the Omnibox
  * Integrated Sync into new settings pages
  * Improved screen reader support
  * New warning when hitting Command-Q on Mac
  * Removal of Google Gears
- security fixes
  * [73962] [79746] High CVE-2011-1808: Use-after-free due to integer issues
    in float handling
  * [75496] Medium CVE-2011-1809: Use-after-free in accessibility support
  * [75643] Low CVE-2011-1810: Visit history information leak in CSS
  * [76034] Low CVE-2011-1811: Browser crash with lots of form submissions
  * [77026] Medium CVE-2011-1812: Extensions permission bypass
  * [78516] High CVE-2011-1813: Stale pointer in extension framework
  * [79362] Medium CVE-2011-1814: Read from uninitialized pointer
  * [79862] Low CVE-2011-1815: Extension script injection into new tab page
  * [80358] Medium CVE-2011-1816: Use-after-free in developer tools
  * [81916] Medium CVE-2011-1817: Browser memory corruption in history
    deletion
  * [81949] High CVE-2011-1818: Use-after-free in image loader
  * [83010] Medium CVE-2011-1819: Extension injection into chrome:// pages
  * [83275] High CVE-2011-2332: Same origin bypass in v8
  * [83743] High CVE-2011-2342: Same origin bypass in DOM
- copy release 12.0.742.91 from beta to stable

* Wed May 25 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.71-1
+ Revision: 678989
- new upstream release 11.0.696.71 (stable)
- security fixes
  * [72189] Low CVE-2011-1801: Pop-up blocker bypass.
  * [$1000] [82546] High CVE-2011-1804: Stale pointer in floats rendering.
  * [82873] Critical CVE-2011-1806: Memory corruption in GPU command buffer.
  * [82903] Critical CVE-2011-1807: Out-of-bounds write in blob handling.
- bug fixes
  * REGRESSION: selection extended by arrow keys flickers on LinkedIn.com.
    (Issue 83197).
  * Have ConnectBackupJob try IPv4 first to hide potential long IPv6 connect
    timeout (Issue 81686).

* Thu May 12 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.68-1
+ Revision: 673982
- new upstream release 11.0.696.68 (stable)
- security fixes
  * [64046] High CVE-2011-1799: Bad casts in Chromium WebKit glue.
  * [80608] High CVE-2011-1800: Integer overflows in SVG filters.

* Sat May 07 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.65-1
+ Revision: 671613
- new upstream release 11.0.696.65 (stable)
  * fix issue 80580: After deleting bookmarks on the Bookmark managers,
    the bookmark bar doesn't display properly with existing bookmarks.

* Fri Apr 29 2011 Claudio Matsuoka <claudio@mandriva.com> 11.0.696.57-1
+ Revision: 660171
- new upstream release 11.0.696.57 (stable)
- security fixes:
  * [61502] High CVE-2011-1303: Stale pointer in floating object handling
  * [70538] Low CVE-2011-1304: Pop-up block bypass via plug-ins
  * [70589] Medium CVE-2011-1305: Linked-list race in database handling
  * [71686] Medium CVE-2011-1434: Lack of thread safety in MIME handling
  * [72523] Medium CVE-2011-1435: Bad extension with tabs permission can
    capture local files
  * [72910] Low CVE-2011-1436: Possible browser crash due to bad interaction
    with X
  * [73526] High CVE-2011-1437: Integer overflows in float rendering
  * [74653] High CVE-2011-1438: Same origin policy violation with blobs
  * [74763] High CVE-2011-1439: Prevent interference between renderer
    processes
  * [75186] High CVE-2011-1440: Use-after-free with <ruby> tag and CSS
  * [75347] High CVE-2011-1441: Bad cast with floating select lists
  * [75801] High CVE-2011-1442: Corrupt node trees with mutation events
  * [76001] High CVE-2011-1443: Stale pointers in layering code
  * [76542] High CVE-2011-1444: Race condition in sandbox launcher
  * [76646] Medium CVE-2011-1445: Out-of-bounds read in SVG
  * [76666] [77507] [78031] High CVE-2011-1446: Possible URL bar spoofs with
    navigation errors and interrupted loads
  * [76966] High CVE-2011-1447: Stale pointer in drop-down list handling
  * [77130] High CVE-2011-1448: Stale pointer in height calculations
  * [77346] High CVE-2011-1449: Use-after-free in WebSockets
  * [77349] Low CVE-2011-1450: Dangling pointers in file dialogs
  * [77463] High CVE-2011-1451: Dangling pointers in DOM id map
  * [77786] Medium CVE-2011-1452: URL bar spoof with redirect and manual
    reload
  * [79199] High CVE-2011-1454: Use-after-free in DOM id handling
  * [79361] Medium CVE-2011-1455: Out-of-bounds read with multipart-encoded
    PDF
  * [79364] High CVE-2011-1456: Stale pointers with PDF forms
- detailed changelog at http://goo.gl/arI9m
- copy Chromium 11 sources from beta to stable
- remove Chromium 10 source files

* Fri Apr 15 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.205-1
+ Revision: 653084
- new upstream release 10.0.648.205 (stable)
  * Fix issue 75629: CVE-2011-1301: Use-after-free in the GPU process
  * Fix issue 78524: CVE-2011-1302: Heap overflow in the GPU process
- detailed changelog at http://goo.gl/wJg8b

* Mon Apr 04 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.204-2
+ Revision: 650370
- update chromium-browser package group
- bump release for buildsystem debug

* Fri Mar 25 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.204-1
+ Revision: 648498
- new upstream release 10.0.648.204 (stable)
  * support for password manager
  * performance and stability fixes
  * fix CVE-2011-1291: Buffer error in base string handling
  * fix CVE-2011-1292: Use-after-free in the frame loader
  * fix CVE-2011-1293: Use-after-free in HTMLCollection
  * fix CVE-2011-1294: Stale pointer in CSS handling
  * fix CVE-2011-1295: DOM tree corruption with broken node parentage
  * fix CVE-2011-1296: Stale pointer in SVG text handling
- fix some system library settings introduced in revision 647139

  + Funda Wang <fwang@mandriva.org>
    - build with more system libs

* Fri Mar 18 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.151-1
+ Revision: 646282
- new upstream release 10.0.648.151 (stable)
  * blacklist a small number of HTTPS certificates

* Sat Mar 12 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.133-1
+ Revision: 644042
- new upstream release 10.0.648.133 (stable)
  * [CVE-2011-1290] fix memory corruption in style handling
- check presence of patch files

* Fri Mar 11 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.127-2
+ Revision: 643848
- apply patches correctly

* Wed Mar 09 2011 Claudio Matsuoka <claudio@mandriva.com> 10.0.648.127-1
+ Revision: 643105
- new upstream release 10.0.648.127 (stable)
  * New version of V8 which greatly improves javascript performance
  * New settings pages that open in a tab, rather than a dialog box
  * Improved security with malware reporting and disabling outdated plugins
    by default
  * Password sync as part of Chrome Sync now enabled by default
  * GPU Accelerated Video
  * Background WebApps
  * webNavigation extension API
- annoucement and security fix list: http://goo.gl/PWdBi
- move chromium patch 10.0.648.114 from beta channel to stable
- move chromium patch 10.0.648.82 from beta channel to stable
- move chromium patch 10.0.648.127 from beta channel to stable
- move chromium patch 10.0.648.126 from beta channel to stable
- move chromium 10.0.648.45 from beta channel to stable
- move patch from beta channel to stable
- move patch from beta channel to stable

* Tue Mar 01 2011 Claudio Matsuoka <claudio@mandriva.com> 9.0.597.107-1
+ Revision: 641075
- new upstream release 9.0.597.107 (stable)
- contains security fixes, see detais at http://goo.gl/rkTSm
- add beta browser to the downgrade notice in spec description

* Sat Feb 12 2011 Claudio Matsuoka <claudio@mandriva.com> 9.0.597.98-1
+ Revision: 637364
- new upstream version 9.0.597.98
- add conflicts to beta channel browser
- add obsoletes entry for old (canary) chromium-browser package

* Thu Feb 10 2011 Claudio Matsuoka <claudio@mandriva.com> 9.0.597.94-1
+ Revision: 637082
- imported package chromium-browser-stable
