%define name pulseaudio
%define version 0.9.16
%define git 0
%define rel 0.test1.1
%if %{git}
%define release %mkrel 0.%{git}.%rel
%else
%define release %mkrel %rel
%endif

# (cg) Lennart has introduced a circular dependancy in the libraries
# libpulse requires libpulsecommon but libpulsecommon requires libpulse.
# This breaks no-undefined.
# Further issues in some test apps (maybe more) require that as-needed is required.
%define _disable_ld_no_undefined 1
%define _disable_ld_as_needed 1
%define _requires_exceptions devel(libpulsecommon

# Majors
%define major 0
%define zeroconfmajor 0
%define glib2major 0
%define apiver %{version}

# Library names
%define libname %mklibname %{name} %{major}
%define libname_devel %mklibname -d %{name}

%define zeroconflibname %mklibname pulsezeroconf %{zeroconfmajor}
%define glib2libname %mklibname pulseglib2 %{glib2major}


Summary: Sound server for Linux
Name: %{name}
Version: %{version}
Release: %{release}
%if %{git}
Source0: %{name}-%{git}.tar.lzma
%else
Source0: %{name}-%{version}-test1.tar.gz
%endif
Source1: %{name}.sysconfig
Source2: %{name}.xinit
# (cg) We have to ship an esd.conf file with auto_spawn=0 to stop
# libesound from.... you guessed it... auto spawning.
Source3: esd.conf
Source4: %{name}.svg


# (cg) Using git to manage patches
# To recreate the structure
# git clone git://git.0pointer.de/pulseaudio
# git checkout v0.9.15
# git checkout -b mdv-0.9.15-cherry-picks
# git am 00*.patch
# git checkout -b mdv-0.9.15-patches
# git am 05*.patch

# To apply new custom patches
# git checkout mdv-0.9.15-patches
# (do stuff)

# To apply new cherry-picks
# git checkout mdv-0.9.15-cherry-picks
# git cherry-pick <blah>
# git checkout mdv-0.9.15-patches
# git rebase mdv-0.9.15-cherry-picks

# Cherry Pick Patches
# git format-patch --start-number 100 v0.9.16..mdv-0.9.16-cherry-picks

# Not currently reverting:
# This is being tracked in https://qa.mandriva.com/show_bug.cgi?id=49947
# This commit seems to have caused problems in skype, so we'll try without
# it and see what the users say :)

# This reverts commit a4cea4e469d3baf27890820eba030b7acdf63daa.

# Mandriva Patches
# git format-patch --start-number 500 mdv-0.9.16-cherry-picks..mdv-0.9.16-patches
Patch500: 0500-Customise-startup-so-we-can-easily-disable-PA.patch
Patch501: 0501-Some-customisations-to-esdcompat-in-order-to-adhere-.patch
Patch502: 0502-Change-the-default-resample-method-to-speex-fixed-0-.patch
Patch503: 0503-start-PA-earlier-in-GNOME-Mdv-bug-47594.patch

# Airtunes links to OpenSSL which is BSD-like and should be reflected here
License: LGPL and BSD-like
Group: Sound
Url: http://pulseaudio.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: glib2-devel
BuildRequires: libcap-devel
BuildRequires: libsndfile-devel
BuildRequires: libsamplerate-devel
BuildRequires: libalsa-devel
BuildRequires: libjack-devel
BuildRequires: libavahi-client-devel
BuildRequires: liboil-devel
BuildRequires: libGConf2-devel
BuildRequires: libwrap-devel
BuildRequires: X11-devel
BuildRequires: udev-devel
BuildRequires: hal-devel
#gw libtool dep:
BuildRequires: dbus-glib-devel
BuildRequires: doxygen
BuildRequires: automake1.8
BuildRequires: libltdl-devel
BuildRequires: libatomic_ops-devel
BuildRequires: gettext-devel
BuildRequires: lirc-devel
BuildRequires: bluez-devel
BuildRequires: tdb-devel
BuildRequires: speex-devel
# (cg) Needed for airtunes
BuildRequires: openssl-devel
%if %{mdkversion} > 200800
BuildRequires: polkit-devel
%endif
#BuildRequires: libasyncns-devel
BuildRequires: intltool
BuildRequires: imagemagick

Provides: polypaudio
Obsoletes: polypaudio
# (cg) This is for the backport of 0.9.7 to 2008
#      pulseaudio fails when using older versions of libtool
Requires: libltdl >= 1.5.24
# (cg) Just incase people backport, require specific udev
Requires: udev >= 143
Requires: rtkit
# (cg) When upgrading from pa < 0.9.7-1 things break due to spec restructure
Conflicts: %{libname} < 0.9.7-2
# (cg) libpulsecore has been moved to a dlopen'ed system.
Obsoletes: %mklibname pulsecore 1
Obsoletes: %mklibname pulsecore 2
Obsoletes: %mklibname pulsecore 3
Obsoletes: %mklibname pulsecore 4
Obsoletes: %mklibname pulsecore 5
Obsoletes: %mklibname pulsecore 6
Obsoletes: %mklibname pulsecore 7
Obsoletes: %mklibname pulsecore 8

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
Summary: Libraries for PulseAudio clients
Group: System/Libraries

%description -n %{libname}
This package contains the runtime libraries for any application that wishes
to interface with a PulseAudio sound server.

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%package -n %{zeroconflibname}
Summary:    Zeroconf support for PulseAudio clients
Group:      System/Libraries

%description -n %{zeroconflibname}
This package contains the runtime libraries and tools that allow PulseAudio
clients to automatically detect PulseAudio servers using Zeroconf.

%post -n %{zeroconflibname} -p /sbin/ldconfig
%postun -n %{zeroconflibname} -p /sbin/ldconfig


%package -n %{glib2libname}
Summary:  GLIB 2.x bindings for PulseAudio clients
Group:    System/Libraries

%description -n %{glib2libname}
This package contains bindings to integrate the PulseAudio client library with
a GLIB 2.x based application.

%post -n %{glib2libname} -p /sbin/ldconfig
%postun -n %{glib2libname} -p /sbin/ldconfig


%package -n %{libname_devel}
Summary: Headers and libraries for PulseAudio client development
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Requires: %{zeroconflibname} = %{version}-%{release}
Requires: %{glib2libname} = %{version}-%{release}
Provides: lib%{name}-devel = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Obsoletes: %mklibname -d %{name} %{major}

%description -n %{libname_devel}
Headers and libraries for developing applications that can communicate with
a PulseAudio sound server.


%package esound-compat
Summary:   PulseAudio EsounD daemon compatibility script
Group:     Sound
Requires:  %{name} = %{version}-%{release}
%if %{mdkversion} > 200800
Provides:  esound
Obsoletes: esound < 0.2.38-5mdv
Conflicts: esound-daemon
%endif

%description esound-compat
A compatibility script that allows applications to call /usr/bin/esd
and start PulseAudio with EsounD protocol modules.


%package module-lirc
Summary:   LIRC support for the PulseAudio sound server
Group:     Sound
Requires:  %{name} = %{version}-%{release}

%description module-lirc
LIRC volume control module for the PulseAudio sound server.


%package module-bluetooth
Summary:   Bluetooth support for the PulseAudio sound server
Group:     Sound
Requires:  %{name} = %{version}-%{release}

%description module-bluetooth
Bluetooth modules for the PulseAudio sound server to provide support
for headsets and proximity detection.


%package module-x11
Summary:   X11 support for the PulseAudio sound server
Group:     Sound
Requires:  %{name} = %{version}-%{release}

%description module-x11
X11 bell and security modules for the PulseAudio sound server.


%package module-zeroconf
Summary:   Zeroconf support for the PulseAudio sound server
Group:     Sound
Requires:  %{name} = %{version}-%{release}

%description module-zeroconf
Zeroconf publishing module for the PulseAudio sound server.


%package module-jack
Summary:   JACK support for the PulseAudio sound server
Group:     Sound
Requires:  %{name} = %{version}-%{release}

%description module-jack
JACK sink and source modules for the PulseAudio sound server.


%package module-gconf
Summary:   GConf support for the PulseAudio sound server
Group:     Sound
Requires:  %{name} = %{version}-%{release}

%description module-gconf
GConf configuration backend for the PulseAudio sound server.


%package utils
Summary:  PulseAudio sound server utilities
Group:    Sound

%description utils
This package contains command line utilities for the PulseAudio sound server.




%prep
%if %{git}
%setup -q -n %{name}-%{git}
%else
%setup -q -n %{name}-%{version}-test1
%endif

%apply_patches

%if %{git}
echo "clean:" > Makefile
./bootstrap.sh -V
%endif

%build
%configure2_5x --disable-asyncns

%make
make doxygen

%install
rm -rf %{buildroot}
%makeinstall_std

install -D -m 0644 %{_sourcedir}/%{name}.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -D -m 0755 %{_sourcedir}/%{name}.xinit %{buildroot}%{_sysconfdir}/X11/xinit.d/50%{name}
install -D -m 0755 %{_sourcedir}/esd.conf %{buildroot}%{_sysconfdir}/

install -D -m 0644 %{_sourcedir}/%{name}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/devices
ln -s ../apps/%{name}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/devices/audio-backend-pulseaudio.svg
for size in 16 22 32 48 64 128; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/{apps,devices}
  convert -geometry ${size}x${size} %{_sourcedir}/%{name}.svg %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/%{name}.png
  ln -s ../apps/%{name}.png %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/devices/audio-backend-pulseaudio.png
done

# Remove static and metalink libraries
find %{buildroot} \( -name *.a -o -name *.la \) -exec rm {} \;

# Fix esd
ln -s esdcompat %{buildroot}%{_bindir}/esd

%find_lang %{name}

%clean
rm -rf %{buildroot}




%files -f %{name}.lang
%defattr(-,root,root)
%doc README
%dir %{_sysconfdir}/pulse/
%config(noreplace) %{_sysconfdir}/pulse/client.conf
%config(noreplace) %{_sysconfdir}/pulse/daemon.conf
%config(noreplace) %{_sysconfdir}/pulse/default.pa
%config(noreplace) %{_sysconfdir}/pulse/system.pa
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(4755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man5/pulse-client.conf.5.*
%{_mandir}/man5/pulse-daemon.conf.5.*
%{_mandir}/man5/default.pa.5.*
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
%{_libdir}/pulse-%{apiver}/modules/module-cork-music-on-phone.so
%{_libdir}/pulse-%{apiver}/modules/module-console-kit.so
%{_libdir}/pulse-%{apiver}/modules/module-detect.so
%{_libdir}/pulse-%{apiver}/modules/module-device-restore.so
%{_libdir}/pulse-%{apiver}/modules/module-esound-compat-spawnfd.so
%{_libdir}/pulse-%{apiver}/modules/module-esound-compat-spawnpid.so
%{_libdir}/pulse-%{apiver}/modules/module-esound-protocol-tcp.so
%{_libdir}/pulse-%{apiver}/modules/module-esound-protocol-unix.so
%{_libdir}/pulse-%{apiver}/modules/module-esound-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-hal-detect.so
%{_libdir}/pulse-%{apiver}/modules/module-http-protocol-tcp.so
%{_libdir}/pulse-%{apiver}/modules/module-http-protocol-unix.so
%{_libdir}/pulse-%{apiver}/modules/module-intended-roles.so
%{_libdir}/pulse-%{apiver}/modules/module-match.so
%{_libdir}/pulse-%{apiver}/modules/module-mmkbd-evdev.so
%{_libdir}/pulse-%{apiver}/modules/module-native-protocol-fd.so
%{_libdir}/pulse-%{apiver}/modules/module-native-protocol-tcp.so
%{_libdir}/pulse-%{apiver}/modules/module-native-protocol-unix.so
%{_libdir}/pulse-%{apiver}/modules/module-null-sink.so
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
%{_libdir}/pulse-%{apiver}/modules/module-udev-detect.so
%{_libdir}/pulse-%{apiver}/modules/module-volume-restore.so
%{_libdir}/pulse-%{apiver}/modules/module-stream-restore.so
%{_libdir}/pulse-%{apiver}/modules/module-suspend-on-idle.so
%{_libdir}/pulse-%{apiver}/modules/module-default-device-restore.so
%{_libdir}/pulse-%{apiver}/modules/module-ladspa-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-remap-sink.so


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libpulse.so.%{major}*
%{_libdir}/libpulse-simple.so.%{major}*
%{_libdir}/libpulsecommon-%{apiver}.so
%{_libdir}/libpulsecore-%{apiver}.so
# (cg) Although the following is not a shared library, putting this file here
# will allow padsp to work on dual arch machines... (e.g. using padsp to start
# a 32-bit app).
%{_libdir}/libpulsedsp.so


%files -n %{zeroconflibname}
%defattr(-,root,root)
%{_libdir}/libpulse-browse.so.%{zeroconfmajor}*


%files -n %{glib2libname}
%defattr(-,root,root)
%{_libdir}/libpulse-mainloop-glib.so.%{glib2major}*

%files -n %{libname_devel}
%doc doxygen/html
%defattr(-,root,root)
%{_libdir}/libpulse.so
%{_libdir}/libpulse-browse.so
%{_libdir}/libpulse-mainloop-glib.so
%{_libdir}/libpulse-simple.so
%dir %{_includedir}/pulse
%{_includedir}/pulse/*.h
%{_libdir}/pkgconfig/*.pc


%files esound-compat
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/esd.conf
%{_bindir}/esdcompat
%{_bindir}/esd
%{_mandir}/man1/esdcompat.1.*

%files module-bluetooth
%defattr(-,root,root)
%{_libdir}/pulse-%{apiver}/modules/libbluetooth-ipc.so
%{_libdir}/pulse-%{apiver}/modules/libbluetooth-sbc.so
%{_libdir}/pulse-%{apiver}/modules/libbluetooth-util.so
%{_libdir}/pulse-%{apiver}/modules/module-bluetooth-device.so
%{_libdir}/pulse-%{apiver}/modules/module-bluetooth-discover.so
%{_libdir}/pulse-%{apiver}/modules/module-bluetooth-proximity.so
%{_libdir}/pulse/proximity-helper


%files module-lirc
%defattr(-,root,root)
%{_libdir}/pulse-%{apiver}/modules/module-lirc.so


%files module-x11
%defattr(-,root,root)
%{_sysconfdir}/X11/xinit.d/50%{name}
%{_bindir}/pax11publish
%{_bindir}/start-pulseaudio-x11
%{_mandir}/man1/pax11publish.1.*
%{_libdir}/pulse-%{apiver}/modules/module-x11-bell.so
%{_libdir}/pulse-%{apiver}/modules/module-x11-cork-request.so
%{_libdir}/pulse-%{apiver}/modules/module-x11-publish.so
%{_libdir}/pulse-%{apiver}/modules/module-x11-xsmp.so
%{_sysconfdir}/xdg/autostart/pulseaudio.desktop


%files module-zeroconf
%defattr(-,root,root)
%{_bindir}/pabrowse
%{_mandir}/man1/pabrowse.1.*
%{_libdir}/pulse-%{apiver}/modules/libavahi-wrap.so
%{_libdir}/pulse-%{apiver}/modules/module-zeroconf-discover.so
%{_libdir}/pulse-%{apiver}/modules/module-zeroconf-publish.so
%{_libdir}/pulse-%{apiver}/modules/module-raop-discover.so


%files module-jack
%defattr(-,root,root)
%{_libdir}/pulse-%{apiver}/modules/module-jack-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-jack-source.so


%files module-gconf
%defattr(-,root,root)
%{_libdir}/pulse-%{apiver}/modules/module-gconf.so
%dir %{_libdir}/pulse/
%{_libdir}/pulse/gconf-helper


%files utils
%defattr(-,root,root)
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
