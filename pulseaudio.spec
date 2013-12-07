%bcond_with	bootstrap

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
%define apiver 4.0

# Library names
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

%define glib2libname %mklibname pulseglib2 %{glib2major}

Summary:	Sound server for Linux
Name:		pulseaudio
Version:	4.0
#Release:	%{?git:0.%{git}.}1
Release:	6
License:	LGPLv2+
Group:		Sound
Url:		http://pulseaudio.org/
#Source0:	%{name}-%{version}%{?git:-%{git}}.tar.xz
Source0:	http://freedesktop.org/software/pulseaudio/releases/%{name}-%{version}.tar.xz
Source1:	%{name}.sysconfig
Source2:	%{name}.xinit
# (cg) We have to ship an esd.conf file with auto_spawn=0 to stop
# libesound from.... you guessed it... auto spawning.
Source3:	esd.conf
Source4:	%{name}.svg

# (cg) Using git to manage patches
# To recreate the structure
# git clone git://git.0pointer.de/pulseaudio
# git checkout v0.9.22
# git checkout -b mdv-0.9.22-cherry-picks
# git am 00*.patch
# git checkout -b mdv-0.9.22-patches
# git am 05*.patch

# To apply new custom patches
# git checkout mdv-0.9.22-patches
# (do stuff)

# To apply new cherry-picks
# git checkout mdv-0.9.22-cherry-picks
# git cherry-pick <blah>
# git checkout mdv-0.9.22-patches
Patch500:	0500-Customise-startup-so-we-can-easily-disable-PA.patch
Patch501:	0501-Some-customisations-to-esdcompat-in-order-to-adhere-.patch
Patch502:	0502-Change-the-default-resample-method-to-speex-fixed-0-.patch
#Patch503:	0503-start-PA-earlier-in-GNOME-Mdv-bug-47594.patch
Patch504:	0504-Apply-startup-customisation-to-new-KDE-module.patch
Patch505:	0505-alsa-mixer-Allow-speakers-even-when-no-specific-path.patch# git rebase mdv-0.9.22-cherry-picks

# Stable Branch Patches
# git format-patch --start-number 100 v0.9.22..stable-queue

# Mandriva Patches
# git format-patch --start-number 500 0.9.22-stable..mdv-0.9.22-patches


# Fix build with >= libudev.so.1
#Patch600:	0001-Remove-usage-of-deprecated-udev_get_-_path.patch

BuildRequires:	doxygen
BuildRequires:	imagemagick
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	cap-devel
BuildRequires:	gettext-devel
BuildRequires:	libatomic_ops-devel
BuildRequires:	libtool-devel
BuildRequires:	wrap-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(avahi-client)
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
# (cg) Needed for airtunes
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(udev) >= 186
BuildRequires:	pkgconfig(orc-0.4)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(tdb)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(xcb-util)
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
# (cg) When upgrading from pa < 0.9.7-1 things break due to spec restructure
Conflicts:	%{libname} < 0.9.7-2
Obsoletes:	%{mklibname pulsezeroconf 0} < 1.0
# (cg) libpulsecore has been moved to a dlopen'ed system.
Obsoletes:	%mklibname pulsecore 1
Obsoletes:	%mklibname pulsecore 2
Obsoletes:	%mklibname pulsecore 3
Obsoletes:	%mklibname pulsecore 4
Obsoletes:	%mklibname pulsecore 5
Obsoletes:	%mklibname pulsecore 6
Obsoletes:	%mklibname pulsecore 7
Obsoletes:	%mklibname pulsecore 8

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
Suggests:	%{mklibname alsa-plugins}-pulseaudio
%ifarch x86_64
# (cg) Suggest the 32 bit library on 64 bits to ensure compatibility
#      with (typically closed source) 32 bit apps.
Suggests:	libpulse.so.0
%endif

%description -n	%{libname}
This package contains the runtime libraries for any application that wishes
to interface with a PulseAudio sound server.

%define alt_name soundprofile
%define alt_priority 20

%package client-config
Summary:	Client configuration for PulseAudio clients
Group:		System/Libraries
Requires:	alsa-plugins-pulse-config
Requires(post):	ccp
Requires(post):	update-alternatives
Requires(postun):	update-alternatives
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
%setup -q -n %{name}-%{version}%{?git:-%{git}}
%apply_patches

# (cg) If autoconf is retriggered (which can happen automatically) we need this file.
cat >git-version-gen <<EOF
#!/bin/bash
echo -n %{version}.0-%{release}
EOF
chmod a+x git-version-gen

%if %{?git}0
echo "clean:" > Makefile
./bootstrap.sh -V
%endif

%build
# (tpg) kill rpaths
%if "%{_libdir}" != "/usr/lib"
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif

%configure2_5x \
        --disable-static \
%ifarch %{arm}
	--disable-neon-opt \
%endif
        --enable-systemd

%make
make doxygen

%install
%makeinstall_std

install -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -D -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/X11/xinit.d/50%{name}
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

%find_lang %{name}

%post
ccp -i -d --set NoOrphans --oldfile %{_sysconfdir}/pulse/daemon.conf --newfile %{_sysconfdir}/pulse/daemon.conf.rpmnew

%post client-config
%{_sbindir}/update-alternatives \
  --install %{_sysconfdir}/sound/profiles/current %{alt_name} %{_sysconfdir}/sound/profiles/pulse %{alt_priority}
ccp -i -d --set NoOrphans --oldfile %{_sysconfdir}/pulse/client.conf --newfile %{_sysconfdir}/pulse/client.conf.rpmnew

%postun client-config
if [ ! -f %{_sysconfdir}/sound/profiles/pulse/profile.conf ]; then
  /usr/sbin/update-alternatives --remove %{alt_name} %{_sysconfdir}/sound/profiles/pulse
fi

%files -f %{name}.lang
%doc README
%dir %{_sysconfdir}/pulse/
%dir %{_libdir}/pulse-%{apiver}
%config(noreplace) %{_sysconfdir}/pulse/daemon.conf
%config(noreplace) %{_sysconfdir}/pulse/default.pa
%config(noreplace) %{_sysconfdir}/pulse/system.pa
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sysconfdir}/bash_completion.d/%{name}-bash-completion.sh
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man5/pulse-client.conf.5.*
%{_mandir}/man5/pulse-daemon.conf.5.*
%{_mandir}/man5/default.pa.5.*
%{_mandir}/man5/pulse-cli-syntax.5.*
%{_datadir}/icons/hicolor/*
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/alsa-mixer
/lib/udev/rules.d/90-pulseaudio.rules
%dir %{_libdir}/pulse-%{apiver}/modules/
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
%{_libdir}/pulse-%{apiver}/modules/module-switch-on-port-available.so
%{_libdir}/pulse-%{apiver}/modules/module-virtual-surround-sink.so
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
%{_libdir}/pulse-%{apiver}/modules/module-systemd-login.so
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
%{_libdir}/pulse-%{apiver}/modules/module-udev-detect.so
%{_libdir}/pulse-%{apiver}/modules/module-volume-restore.so
%{_libdir}/pulse-%{apiver}/modules/module-virtual-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-virtual-source.so
%{_libdir}/pulse-%{apiver}/modules/module-stream-restore.so
%{_libdir}/pulse-%{apiver}/modules/module-suspend-on-idle.so
%{_libdir}/pulse-%{apiver}/modules/module-default-device-restore.so
%{_libdir}/pulse-%{apiver}/modules/module-ladspa-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-remap-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-switch-on-connect.so
%{_libdir}/pulse-%{apiver}/modules/module-filter-apply.so
%{_libdir}/pulse-%{apiver}/modules/module-filter-heuristics.so
%{_libdir}/pulse-%{apiver}/modules/module-remap-source.so
%{_libdir}/pulse-%{apiver}/modules/module-role-ducking.so

%files -n %{libname}
%{_libdir}/libpulse.so.%{major}*
%{_libdir}/libpulse-simple.so.%{major}*
%{_libdir}/pulseaudio/libpulsecommon-%{apiver}.so
%{_libdir}/pulseaudio/libpulsedsp.so
%{_libdir}/libpulsecore-%{apiver}.so
# (cg) Although the following is not a shared library, putting this file here
# will allow padsp to work on dual arch machines... (e.g. using padsp to start
# a 32-bit app).

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
%{_libdir}/cmake/PulseAudio
%{_includedir}/pulse/*.h
%{_libdir}/pkgconfig/*.pc
%{_datadir}/vala/vapi/libpulse.deps
%{_datadir}/vala/vapi/libpulse.vapi
%{_datadir}/vala/vapi/libpulse-mainloop-glib.deps
%{_datadir}/vala/vapi/libpulse-mainloop-glib.vapi

%files esound-compat
%config(noreplace) %{_sysconfdir}/esd.conf
%{_bindir}/esdcompat
%{_bindir}/esd
%{_mandir}/man1/esdcompat.1.*

%if !%{with bootstrap}
%files module-bluetooth
%{_libdir}/pulse-%{apiver}/modules/libbluetooth-util.so
%{_libdir}/pulse-%{apiver}/modules/module-bluetooth-device.so
%{_libdir}/pulse-%{apiver}/modules/module-bluetooth-discover.so
%{_libdir}/pulse-%{apiver}/modules/module-bluetooth-proximity.so
%{_libdir}/pulse-%{apiver}/modules/module-bluetooth-policy.so
%{_libdir}/pulse/proximity-helper
%endif

%files module-lirc
%{_libdir}/pulse-%{apiver}/modules/module-lirc.so

%files module-x11
%{_sysconfdir}/X11/xinit.d/50%{name}
%{_bindir}/pax11publish
%{_bindir}/start-pulseaudio-x11
%{_bindir}/start-pulseaudio-kde
%{_mandir}/man1/pax11publish.1.*
%{_mandir}/man1/start-pulseaudio-x11.1.*
%{_mandir}/man1/start-pulseaudio-kde.1.*
%{_libdir}/pulse-%{apiver}/modules/module-x11-bell.so
%{_libdir}/pulse-%{apiver}/modules/module-x11-cork-request.so
%{_libdir}/pulse-%{apiver}/modules/module-x11-publish.so
%{_libdir}/pulse-%{apiver}/modules/module-x11-xsmp.so
%{_sysconfdir}/xdg/autostart/pulseaudio.desktop
%{_sysconfdir}/xdg/autostart/pulseaudio-kde.desktop

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
%dir %{_libdir}/pulse/
%{_libdir}/pulse/gconf-helper

%files module-equalizer
%{_bindir}/qpaeq
%{_libdir}/pulse-%{apiver}/modules/module-equalizer-sink.so

%ifarch %{ix86} x86_64 ia64
%{_libdir}/pulse-%{apiver}/modules/module-xenpv-sink.so
%endif

%files utils
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
%{_mandir}/man1/pacmd.1.*
%{_mandir}/man1/pactl.1.*
%{_mandir}/man1/padsp.1.*
%{_mandir}/man1/paplay.1.*
%{_mandir}/man1/pasuspender.1.*

