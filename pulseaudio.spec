%define fullgit f81e3e1d7852c05b4b737ac7dac4db95798f0117
#define git 0

%bcond_with bootstrap

# (cg) Lennart has introduced a circular dependancy in the libraries
# libpulse requires libpulsecommon but libpulsecommon requires libpulse.
# This breaks no-undefined.
# Further issues in some test apps (maybe more) require that disabling
# as-needed is also required.
%define _disable_ld_no_undefined 1
%define _disable_ld_as_needed 1
%define __noautoreq 'devel\\(libpulsecommon

# Majors
%define major 0
%define glib2major 0
%define apiver 11.1

# Library names
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

%define glib2libname %mklibname pulseglib2 %{glib2major}

Summary:	Sound server for Linux
Name:		pulseaudio
Version:	12.0
Release:	1
License:	LGPLv2+
Group:		Sound
Url:		http://pulseaudio.org/
#Source0:	%{name}-%{version}%{?git:-%{git}}.tar.xz
Source0:	http://freedesktop.org/software/pulseaudio/releases/%{name}-%{version}%{?git:-%{fullgit}}.tar.xz
Source1:	%{name}.sysconfig
# (cg) We have to ship an esd.conf file with auto_spawn=0 to stop
# libesound from.... you guessed it... auto spawning.
Source3:	esd.conf
Source4:	%{name}.svg
# Load more modules if they are available
Patch0:		pulseaudio-5.0-defaults.patch
Patch1:		pulseaudio-6.0-kde-delay.patch
# Load device-manager module
Patch3:		pulseaudio-7.1-load-module-device-manager.patch
Patch4:		pulseaudio-11.1-glibc-2.27.patch
Patch501:	0501-Some-customisations-to-esdcompat-in-order-to-adhere-.patch
BuildRequires:	doxygen
BuildRequires:	imagemagick
BuildRequires:	intltool >= 0.51.0
BuildRequires:	libtool
BuildRequires:	cap-devel
BuildRequires:	gettext-devel
BuildRequires:	libatomic_ops-devel
BuildRequires:	libtool-devel
BuildRequires:	wrap-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(avahi-client) avahi-common-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(json-c)
BuildRequires:	pkgconfig(libasyncns)
BuildRequires:	pkgconfig(liblircclient0)
BuildRequires:	pkgconfig(webrtc-audio-processing)
BuildRequires:	pkgconfig(sbc)
BuildRequires:	pkgconfig(soxr)
# (cg) Needed for airtunes
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(udev) >= 186
BuildRequires:	pkgconfig(orc-0.4)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(speexdsp)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(tdb)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(x11-xcb)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xcb-util)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(bash-completion)
%if !%{with bootstrap}
BuildRequires:	pkgconfig(bluez)
%endif

%ifarch %{ix86} x86_64 ia64
BuildRequires:	xen-devel
%endif

%rename		polypaudio
# (cg) Just incase people backport, require specific udev
Requires:	udev >= 143
Requires:	rtkit
Requires(post):	ccp
Requires(post):	rpm-helper
# (cg) When upgrading from pa < 0.9.7-1 things break due to spec restructure
Conflicts:	%{libname} < 0.9.7-2
Obsoletes:	%{mklibname pulsezeroconf 0} < 1.0
# (cg) libpulsecore has been moved to a dlopen'ed system.
Obsoletes:	%{mklibname pulsecore 1}
Obsoletes:	%{mklibname pulsecore 2}
Obsoletes:	%{mklibname pulsecore 3}
Obsoletes:	%{mklibname pulsecore 4}
Obsoletes:	%{mklibname pulsecore 5}
Obsoletes:	%{mklibname pulsecore 6}
Obsoletes:	%{mklibname pulsecore 7}
Obsoletes:	%{mklibname pulsecore 8}
Obsoletes:	%{mklibname pulsecore 7.0} < 8.0
Obsoletes:	%{mklibname pulsecore 7.1} < 8.0
Provides:	%{mklibname pulsecore 7.0} = 8.0
Provides:	%{mklibname pulsecore 7.1} = 8.0
Obsoletes:	%{mklibname pulsezeroconf 0}
Conflicts:	%{libname} < 5.0
Obsoletes:	%{mklibname pulsecommon 7.0} < 8.0
Obsoletes:	%{mklibname pulsecommon 7.1} < 8.0
Provides:	%{mklibname pulsecommon 7.0} = 8.0
Provides:	%{mklibname pulsecommon 7.1} = 8.0
Provides:	%{mklibname pulsecommon 5.0}

%description
pulseaudio is a sound server for Linux and other Unix like operating
systems. It is intended to be an improved drop-in replacement for the
Enlightened Sound Daemon (EsounD). In addition to the features EsounD
provides pulseaudio has:
     * Extensible plugin architecture (by loading dynamic loadable
       modules with dlopen())
     * Support for more than one sink/source
     * Better low latency behaviour
     * Embedabble into other software (the core is available as C
       library)
     * Completely asynchronous C API
     * Simple command line interface for reconfiguring the daemon while
       running
     * Flexible, implicit sample type conversion and resampling
     * "Zero-Copy" architecture
     * Module autoloading
     * Very accurate latency measurement for playback and recording.
     * May be used to combine multiple sound cards to one (with sample
       rate adjustment)
     * Client side latency interpolation

%package -n %{libname}
Summary:	Libraries for PulseAudio clients
Group:		System/Libraries
Requires:	%{name}-client-config

%description -n	%{libname}
This package contains the runtime libraries for any application that wishes
to interface with a PulseAudio sound server.

%define alt_name soundprofile
%define alt_priority 20

%package client-config
Summary:	Client configuration for PulseAudio clients
Group:		System/Libraries
# (proyvind): leave thix as suggests, do not change into requires, otherwise
#             pulseaudio cannot be disabled by default
Suggests:	%{mklibname alsa-plugins}-pulseaudio
Requires(post):	ccp
Requires(post):	chkconfig
Requires(postun):	chkconfig
Conflicts:	%{name} < 0.9.16-0.20090816.1
# (cg) Adding the obsoletes here as this package is almost always installed
#      and doing it in task-pulseaudio would cause it to be installed when not needed.
# Flash plugin support pulse natively and libflashsupport now causes more
# problems than it fixes
Obsoletes:	libflashsupport

%description client-config
This package contains the client configuration files for any application that
wishes to interface with a PulseAudio sound server.

%package -n %{glib2libname}
Summary:	GLIB 2.x bindings for PulseAudio clients
Group:		System/Libraries

%description -n	%{glib2libname}
This package contains bindings to integrate the PulseAudio client library with
a GLIB 2.x based application.

%package -n %{devname}
Summary:	Headers and libraries for PulseAudio client development
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{glib2libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d %{name} %{major}

%description -n	%{devname}
Headers and libraries for developing applications that can communicate with
a PulseAudio sound server.

%package esound-compat
Summary:	PulseAudio EsounD daemon compatibility script
Group:		Sound
Requires:	%{name} = %{version}-%{release}
%rename		esound
%rename		esound-daemon

%description esound-compat
A compatibility script that allows applications to call /usr/bin/esd
and start PulseAudio with EsounD protocol modules.

%package module-lirc
Summary:	LIRC support for the PulseAudio sound server
Group:		Sound
Requires:	%{name} = %{version}-%{release}

%description module-lirc
LIRC volume control module for the PulseAudio sound server.

%if !%{with bootstrap}
%package module-bluetooth
Summary:	Bluetooth support for the PulseAudio sound server
Group:		Sound
Requires:	%{name} = %{version}-%{release}

%description module-bluetooth
Bluetooth modules for the PulseAudio sound server to provide support
for headsets and proximity detection.
%endif

%package module-x11
Summary:	X11 support for the PulseAudio sound server
Group:		Sound
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-utils = %{version}-%{release}

%description module-x11
X11 bell and security modules for the PulseAudio sound server.

%package module-zeroconf
Summary:	Zeroconf support for the PulseAudio sound server
Group:		Sound
Requires:	%{name} = %{version}-%{release}

%description module-zeroconf
Zeroconf publishing module for the PulseAudio sound server.

%package module-jack
Summary:	JACK support for the PulseAudio sound server
Group:		Sound
Requires:	%{name} = %{version}-%{release}

%description module-jack
JACK sink and source modules for the PulseAudio sound server.

%ifarch %{ix86} x86_64 ia64
%package module-xen
Summary:	Xen guest support for the PulseAudio sound server
Group:		Sound/Mixers
Requires:	%{name} = %{version}-%{release}

%description module-xen
Xen guest support for the PulseAudio sound server.
%endif

%package module-gconf
Summary:	GConf support for the PulseAudio sound server
Group:		Sound
Requires:	%{name} = %{version}-%{release}

%description module-gconf
GConf configuration backend for the PulseAudio sound server.

%package module-equalizer
Summary:	Equalizer support for the PulseAudio sound server
Group:		Sound
Requires:	%{name} = %{version}-%{release}

%description module-equalizer
Equalizer support and GUI for the PulseAudio sound server.

%package utils
Summary:	PulseAudio sound server utilities
Group:		Sound

%description utils
This package contains command line utilities for the PulseAudio sound server.

%prep
%setup -q -n %{name}-%{version}%{?git:-%{fullgit}}
%apply_patches

# (cg) If autoconf is retriggered (which can happen automatically) we need this file.
cat >git-version-gen <<EOF
#!/bin/bash
echo -n %{version}.0-%{release}
EOF
chmod a+x git-version-gen

libtoolize --copy --force
autopoint --force
autoreconf --force --install --verbose
intltoolize --automake --copy --force

%if %{?git}0
echo "clean:" > Makefile
./bootstrap.sh -V
%endif

%build
# (tpg) kill rpaths
%if "%{_libdir}" != "/usr/lib"
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif

%configure \
        --disable-static \
	--with-systemduserunitdir=%{_userunitdir} \
        --enable-x11 \
%ifarch %{armx}
	--disable-neon-opt \
%endif
%if !%{with bootstrap}
	--enable-bluez5 \
%endif
	--disable-bluez4

%make
make doxygen

%install
%makeinstall_std

install -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -D -m 0755 %{SOURCE3} %{buildroot}%{_sysconfdir}/
install -D -m 0644 %{SOURCE4} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/devices
ln -s ../apps/%{name}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/devices/audio-backend-pulseaudio.svg
for size in 16 22 32 48 64 128; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/{apps,devices}
  convert -geometry ${size}x${size} %{SOURCE4} %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
  ln -s ../apps/%{name}.png %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/devices/audio-backend-pulseaudio.png
done

# Fix esd
ln -s esdcompat %{buildroot}%{_bindir}/esd

# (cg) For sound profile support
mkdir -p %{buildroot}%{_sysconfdir}/sound/profiles/pulse
echo "SOUNDPROFILE=pulse" >%{buildroot}%{_sysconfdir}/sound/profiles/pulse/profile.conf

# (cg) HAL support is no longer the default, and we don't officially support system wide, so
# System Wide + HAL is pretty unlikely.
rm -f %{buildroot}%{_sysconfdir}/dbus-1/system.d/%{name}-system.conf

# (cg) We require systemd now, so no point in using CK
rm -f %{buildroot}%{_libdir}/pulse-%{apiver}/modules/module-console-kit.so

# (cg) Disable x11-cork-request... it should be ahndled in the apps as we cannot
#      maintain state via this mechanism. Should be a patch, but I'm lazy.
sed -i 's,\(/usr/bin/pactl load-module module-x11-cork-request\),#\1,' %{buildroot}%{_bindir}/start-pulseaudio-x11

# Speed up pulseaudio shutdown so that it exits immediately with
# the last user session (module-systemd-login keeps it alive)
sed -e "/exit-idle-time/iexit-idle-time=0" -i %{buildroot}%{_sysconfdir}/pulse/daemon.conf

# (tpg) enable pulseaudio in userland
mkdir -p %{buildroot}%{_userunitdir}/sockets.target.wants
ln -sf %{_userunitdir}/pulseaudio.socket %{buildroot}%{_userunitdir}/sockets.target.wants/pulseaudio.socket

%find_lang %{name}

%post
ccp -i -d --set NoOrphans --oldfile %{_sysconfdir}/pulse/daemon.conf --newfile %{_sysconfdir}/pulse/daemon.conf.rpmnew
%systemd_user_post pulseaudio.socket

%post client-config
%{_sbindir}/update-alternatives \
  --install %{_sysconfdir}/sound/profiles/current %{alt_name} %{_sysconfdir}/sound/profiles/pulse %{alt_priority}
ccp -i -d --set NoOrphans --oldfile %{_sysconfdir}/pulse/client.conf --newfile %{_sysconfdir}/pulse/client.conf.rpmnew

%postun client-config
if [ ! -f %{_sysconfdir}/sound/profiles/pulse/profile.conf ]; then
  /usr/sbin/update-alternatives --remove %{alt_name} %{_sysconfdir}/sound/profiles/pulse
fi

%triggerin client-config -- %{name}-client-config < 6.0-3
# Autospawn behaviour changed to use systemd, so tidy up the client.conf
# by setting it back to the default value - it no longer changes depending on
# the users soundprofile choice - it always defaults to no.
sed -i 's/^\(\s*\)\;\?\s*\(autospawn\s*=\s*\).*/\1\; \2no/' %{_sysconfdir}/pulse/client.conf

%files -f %{name}.lang
%doc README
%dir %{_sysconfdir}/pulse/
%dir %{_libdir}/pulse-%{apiver}
%config(noreplace) %{_sysconfdir}/pulse/daemon.conf
%config(noreplace) %{_sysconfdir}/pulse/default.pa
%config(noreplace) %{_sysconfdir}/pulse/system.pa
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man5/pulse-client.conf.5.*
%{_mandir}/man5/pulse-daemon.conf.5.*
%{_mandir}/man5/default.pa.5.*
%{_mandir}/man5/pulse-cli-syntax.5.*
%{_datadir}/icons/hicolor/*
%{_datadir}/zsh/site-functions/_pulseaudio
%{_userunitdir}/pulseaudio.service
%{_userunitdir}/pulseaudio.socket
%{_userunitdir}/sockets.target.wants/pulseaudio.socket
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/alsa-mixer
/lib/udev/rules.d/90-pulseaudio.rules

%files -n %{libname}
%{_libdir}/libpulse.so.%{major}*
%{_libdir}/libpulse-simple.so.%{major}*
# Modules go to the library package because 32-bit versions of the libraries
# require 32-bit versions of the core modules.
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libpulsedsp.so
%{_libdir}/%{name}/libpulsecore-%{apiver}.so
%{_libdir}/%{name}/libpulsecommon-%{apiver}.so
%dir %{_libdir}/pulse-%{apiver}/modules/
%{_libdir}/pulse-%{apiver}/modules/module-allow-passthrough.so
%{_libdir}/pulse-%{apiver}/modules/libalsa-util.so
%{_libdir}/pulse-%{apiver}/modules/libcli.so
%{_libdir}/pulse-%{apiver}/modules/liboss-util.so
%{_libdir}/pulse-%{apiver}/modules/libprotocol-cli.so
%{_libdir}/pulse-%{apiver}/modules/libprotocol-esound.so
%{_libdir}/pulse-%{apiver}/modules/libprotocol-http.so
%{_libdir}/pulse-%{apiver}/modules/libprotocol-native.so
%{_libdir}/pulse-%{apiver}/modules/libprotocol-simple.so
%{_libdir}/pulse-%{apiver}/modules/libraop.so
%{_libdir}/pulse-%{apiver}/modules/librtp.so
%{_libdir}/pulse-%{apiver}/modules/libwebrtc-util.so
%{_libdir}/pulse-%{apiver}/modules/module-alsa-card.so
%{_libdir}/pulse-%{apiver}/modules/module-alsa-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-alsa-source.so
%{_libdir}/pulse-%{apiver}/modules/module-always-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-augment-properties.so
%{_libdir}/pulse-%{apiver}/modules/module-card-restore.so
%{_libdir}/pulse-%{apiver}/modules/module-cli-protocol-tcp.so
%{_libdir}/pulse-%{apiver}/modules/module-cli-protocol-unix.so
%{_libdir}/pulse-%{apiver}/modules/module-cli.so
%{_libdir}/pulse-%{apiver}/modules/module-combine.so
%{_libdir}/pulse-%{apiver}/modules/module-combine-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-role-cork.so
%{_libdir}/pulse-%{apiver}/modules/module-systemd-login.so
%{_libdir}/pulse-%{apiver}/modules/module-dbus-protocol.so
%{_libdir}/pulse-%{apiver}/modules/module-detect.so
%{_libdir}/pulse-%{apiver}/modules/module-device-manager.so
%{_libdir}/pulse-%{apiver}/modules/module-device-restore.so
%{_libdir}/pulse-%{apiver}/modules/module-echo-cancel.so
%{_libdir}/pulse-%{apiver}/modules/module-esound-compat-spawnfd.so
%{_libdir}/pulse-%{apiver}/modules/module-esound-compat-spawnpid.so
%{_libdir}/pulse-%{apiver}/modules/module-esound-protocol-tcp.so
%{_libdir}/pulse-%{apiver}/modules/module-esound-protocol-unix.so
%{_libdir}/pulse-%{apiver}/modules/module-esound-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-hal-detect.so
%{_libdir}/pulse-%{apiver}/modules/module-http-protocol-tcp.so
%{_libdir}/pulse-%{apiver}/modules/module-http-protocol-unix.so
%{_libdir}/pulse-%{apiver}/modules/module-intended-roles.so
%{_libdir}/pulse-%{apiver}/modules/module-loopback.so
%{_libdir}/pulse-%{apiver}/modules/module-match.so
%{_libdir}/pulse-%{apiver}/modules/module-mmkbd-evdev.so
%{_libdir}/pulse-%{apiver}/modules/module-native-protocol-fd.so
%{_libdir}/pulse-%{apiver}/modules/module-native-protocol-tcp.so
%{_libdir}/pulse-%{apiver}/modules/module-native-protocol-unix.so
%{_libdir}/pulse-%{apiver}/modules/module-null-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-null-source.so
%{_libdir}/pulse-%{apiver}/modules/module-oss.so
%{_libdir}/pulse-%{apiver}/modules/module-pipe-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-pipe-source.so
%{_libdir}/pulse-%{apiver}/modules/module-raop-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-rygel-media-server.so
%{_libdir}/pulse-%{apiver}/modules/module-position-event-sounds.so
%{_libdir}/pulse-%{apiver}/modules/module-rescue-streams.so
%{_libdir}/pulse-%{apiver}/modules/module-rtp-recv.so
%{_libdir}/pulse-%{apiver}/modules/module-rtp-send.so
%{_libdir}/pulse-%{apiver}/modules/module-simple-protocol-tcp.so
%{_libdir}/pulse-%{apiver}/modules/module-simple-protocol-unix.so
%{_libdir}/pulse-%{apiver}/modules/module-sine.so
%{_libdir}/pulse-%{apiver}/modules/module-sine-source.so
%{_libdir}/pulse-%{apiver}/modules/module-tunnel-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-tunnel-source.so
%{_libdir}/pulse-%{apiver}/modules/module-tunnel-sink-new.so
%{_libdir}/pulse-%{apiver}/modules/module-tunnel-source-new.so
%{_libdir}/pulse-%{apiver}/modules/module-udev-detect.so
%{_libdir}/pulse-%{apiver}/modules/module-volume-restore.so
%{_libdir}/pulse-%{apiver}/modules/module-virtual-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-virtual-source.so
%{_libdir}/pulse-%{apiver}/modules/module-stream-restore.so
%{_libdir}/pulse-%{apiver}/modules/module-suspend-on-idle.so
%{_libdir}/pulse-%{apiver}/modules/module-default-device-restore.so
%{_libdir}/pulse-%{apiver}/modules/module-ladspa-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-remap-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-remap-source.so
%{_libdir}/pulse-%{apiver}/modules/module-switch-on-connect.so
%{_libdir}/pulse-%{apiver}/modules/module-filter-apply.so
%{_libdir}/pulse-%{apiver}/modules/module-filter-heuristics.so
%{_libdir}/pulse-%{apiver}/modules/module-virtual-surround-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-switch-on-port-available.so
%{_libdir}/pulse-%{apiver}/modules/module-role-ducking.so

%files client-config
%config(noreplace) %{_sysconfdir}/pulse/client.conf
%dir %{_sysconfdir}/sound/profiles/pulse
%{_sysconfdir}/sound/profiles/pulse/profile.conf

%files -n %{glib2libname}
%{_libdir}/libpulse-mainloop-glib.so.%{glib2major}*

%files -n %{devname}
%doc doxygen/html
%{_libdir}/libpulse.so
%{_libdir}/libpulse-mainloop-glib.so
%{_libdir}/libpulse-simple.so
%dir %{_includedir}/pulse
%{_includedir}/pulse/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/PulseAudio
%{_datadir}/vala/vapi/libpulse.deps
%{_datadir}/vala/vapi/libpulse.vapi
%{_datadir}/vala/vapi/libpulse-mainloop-glib.deps
%{_datadir}/vala/vapi/libpulse-mainloop-glib.vapi
%{_datadir}/vala/vapi/libpulse-simple.deps
%{_datadir}/vala/vapi/libpulse-simple.vapi

%files esound-compat
%config(noreplace) %{_sysconfdir}/esd.conf
%{_bindir}/esdcompat
%{_bindir}/esd
%{_mandir}/man1/esdcompat.1.*

%if !%{with bootstrap}
%files module-bluetooth
%{_libdir}/pulse-%{apiver}/modules/libbluez5-util.so
%{_libdir}/pulse-%{apiver}/modules/module-bluetooth-discover.so
%{_libdir}/pulse-%{apiver}/modules/module-bluetooth-policy.so
%{_libdir}/pulse-%{apiver}/modules/module-bluez5-device.so
%{_libdir}/pulse-%{apiver}/modules/module-bluez5-discover.so
%endif

%files module-lirc
%{_libdir}/pulse-%{apiver}/modules/module-lirc.so

%files module-x11
%{_bindir}/pax11publish
%{_bindir}/start-pulseaudio-x11
%{_mandir}/man1/pax11publish.1.*
%{_mandir}/man1/start-pulseaudio-x11.1.*
%{_libdir}/pulse-%{apiver}/modules/module-x11-bell.so
%{_libdir}/pulse-%{apiver}/modules/module-x11-cork-request.so
%{_libdir}/pulse-%{apiver}/modules/module-x11-publish.so
%{_libdir}/pulse-%{apiver}/modules/module-x11-xsmp.so
%{_sysconfdir}/xdg/autostart/pulseaudio.desktop

%files module-zeroconf
%{_libdir}/pulse-%{apiver}/modules/libavahi-wrap.so
%{_libdir}/pulse-%{apiver}/modules/module-zeroconf-discover.so
%{_libdir}/pulse-%{apiver}/modules/module-zeroconf-publish.so
%{_libdir}/pulse-%{apiver}/modules/module-raop-discover.so

%files module-jack
%{_libdir}/pulse-%{apiver}/modules/module-jack-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-jack-source.so
%{_libdir}/pulse-%{apiver}/modules/module-jackdbus-detect.so

%files module-gconf
%{_libdir}/pulse-%{apiver}/modules/module-gconf.so
%dir %{_libexecdir}/pulse/
%{_libexecdir}/pulse/gconf-helper

%files module-equalizer
%{_bindir}/qpaeq
%{_libdir}/pulse-%{apiver}/modules/module-equalizer-sink.so

%files utils
%{_datadir}/bash-completion/completions/p*
%{_bindir}/pacat
%{_bindir}/pacmd
%{_bindir}/pactl
%{_bindir}/padsp
%{_bindir}/pamon
%{_bindir}/paplay
%{_bindir}/parec
%{_bindir}/parecord
%{_bindir}/pasuspender
%{_mandir}/man1/pacat.1.*
%{_mandir}/man1/pamon.1.*
%{_mandir}/man1/parec.1.*
%{_mandir}/man1/parecord.1.*
%{_mandir}/man1/pacmd.1.*
%{_mandir}/man1/pactl.1.*
%{_mandir}/man1/padsp.1.*
%{_mandir}/man1/paplay.1.*
%{_mandir}/man1/pasuspender.1.*
