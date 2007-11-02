%define name pulseaudio
%define version 0.9.7
%define rel 5
%define svn 0
%if %{svn}
%define release %mkrel 0.%{svn}.%rel
%else
%define release %mkrel %rel
%endif

# Majors
%define major 0
%define coremajor 4
%define zeroconfmajor 0
%define glib2major 0
%define apiver 0.9

# Library names
%define libname %mklibname %{name} %{major}
%define libname_devel %mklibname -d %{name}
%define corelibname %mklibname pulsecore %{coremajor}
%define zeroconflibname %mklibname pulsezeroconf %{zeroconfmajor}
%define glib2libname %mklibname pulseglib2 %{glib2major}


Summary: Sound server for Linux
Name: %{name}
Version: %{version}
Release: %{release}
%if %{svn}
Source0: %{name}-%{svn}.tar.bz2
%else
Source0: %{name}-%{version}.tar.gz
%endif
License: LGPL
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
BuildRequires: XFree86-devel
BuildRequires: hal-devel
BuildRequires: doxygen
BuildRequires: automake1.8
BuildRequires: libltdl-devel
BuildRequires: libatomic_ops-devel
BuildRequires: gettext-devel
BuildRequires: lirc-devel
#BuildRequires: libasyncns-devel
Provides: polypaudio
Obsoletes: polypaudio
# (cg) This is for the backport of 0.9.7 to 2008
#      pulseaudio fails when using older versions of libtool
Requires: libltdl >= 1.5.24


%description
pulseaudio is a sound server for Linux and other Unix like operating
systems. It is intended to be an improved drop-in replacement for the
Enlightened Sound Daemon (ESOUND). In addition to the features ESOUND
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

%package -n %{corelibname}
Summary: Core libraries for the PulseAudio sound server.
Group: System/Libraries

%description -n %{corelibname}
This package contains runtime libraries that are used internally in the
PulseAudio sound server.

%post -n %{corelibname} -p /sbin/ldconfig
%postun -n %{corelibname} -p /sbin/ldconfig


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
Requires: %{corelibname} = %{version}-%{release}
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
# Wait until we update this properly in esound package
#Provides:  esound
#Obsoletes: esound

%description esound-compat
A compatibility script that allows applications to call /usr/bin/esd
and start PulseAudio with EsounD protocol modules.


%package module-lirc
Summary:   LIRC support for the PulseAudio sound server
Group:     Sound
Requires:  %{name} = %{version}-%{release}

%description module-lirc
LIRC volume control module for the PulseAudio sound server.


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
%if %{svn}
%setup -q -n %{name}
%else
%setup -q
%endif

%build
%if %{svn}
libtoolize --force
NOCONFIGURE=1 ./bootstrap.sh
%endif
%configure2_5x --disable-glib1
make
make doxygen

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
# Remove static and metalink libraries
find %{buildroot} \( -name *.a -o -name *.la \) -exec rm {} \;

# Fix esd
ln -s esdcompat %{buildroot}%{_bindir}/esd
# Unlike most distros we do not patch esound to change the esound socket file
# which as far as I can tell breaks user switching... :s
# We need to use the esd socket favoured by esound
sed -i 's,^\(load-module module-esound-protocol-unix\).*,\1 socket="/tmp/.esd/socket",' %{buildroot}%{_sysconfdir}/pulse/default.pa

%clean
rm -rf $RPM_BUILD_ROOT




%files
%defattr(-,root,root)
%doc README
%dir %{_sysconfdir}/pulse/
%config(noreplace) %{_sysconfdir}/pulse/client.conf
%config(noreplace) %{_sysconfdir}/pulse/daemon.conf
%config(noreplace) %{_sysconfdir}/pulse/default.pa
%attr(4755,root,root) %{_bindir}/%{name}
%dir %{_libdir}/pulse-%{apiver}/modules/
%{_libdir}/pulse-%{apiver}/modules/libalsa-util.so
%{_libdir}/pulse-%{apiver}/modules/libauthkey-prop.so
%{_libdir}/pulse-%{apiver}/modules/libauthkey.so
%{_libdir}/pulse-%{apiver}/modules/libcli.so
%{_libdir}/pulse-%{apiver}/modules/libdbus-util.so
%{_libdir}/pulse-%{apiver}/modules/libiochannel.so
%{_libdir}/pulse-%{apiver}/modules/libioline.so
%{_libdir}/pulse-%{apiver}/modules/libipacl.so
%{_libdir}/pulse-%{apiver}/modules/liboss-util.so
%{_libdir}/pulse-%{apiver}/modules/libpacket.so
%{_libdir}/pulse-%{apiver}/modules/libparseaddr.so
%{_libdir}/pulse-%{apiver}/modules/libpdispatch.so
%{_libdir}/pulse-%{apiver}/modules/libprotocol-cli.so
%{_libdir}/pulse-%{apiver}/modules/libprotocol-esound.so
%{_libdir}/pulse-%{apiver}/modules/libprotocol-http.so
%{_libdir}/pulse-%{apiver}/modules/libprotocol-native.so
%{_libdir}/pulse-%{apiver}/modules/libprotocol-simple.so
%{_libdir}/pulse-%{apiver}/modules/libpstream-util.so
%{_libdir}/pulse-%{apiver}/modules/libpstream.so
%{_libdir}/pulse-%{apiver}/modules/librtp.so
%{_libdir}/pulse-%{apiver}/modules/libsocket-client.so
%{_libdir}/pulse-%{apiver}/modules/libsocket-server.so
%{_libdir}/pulse-%{apiver}/modules/libsocket-util.so
%{_libdir}/pulse-%{apiver}/modules/libstrlist.so
%{_libdir}/pulse-%{apiver}/modules/libtagstruct.so
%{_libdir}/pulse-%{apiver}/modules/module-alsa-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-alsa-source.so
%{_libdir}/pulse-%{apiver}/modules/module-cli-protocol-tcp.so
%{_libdir}/pulse-%{apiver}/modules/module-cli-protocol-unix.so
%{_libdir}/pulse-%{apiver}/modules/module-cli.so
%{_libdir}/pulse-%{apiver}/modules/module-combine.so
%{_libdir}/pulse-%{apiver}/modules/module-detect.so
%{_libdir}/pulse-%{apiver}/modules/module-esound-compat-spawnfd.so
%{_libdir}/pulse-%{apiver}/modules/module-esound-compat-spawnpid.so
%{_libdir}/pulse-%{apiver}/modules/module-esound-protocol-tcp.so
%{_libdir}/pulse-%{apiver}/modules/module-esound-protocol-unix.so
%{_libdir}/pulse-%{apiver}/modules/module-esound-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-hal-detect.so
%{_libdir}/pulse-%{apiver}/modules/module-http-protocol-tcp.so
%{_libdir}/pulse-%{apiver}/modules/module-http-protocol-unix.so
%{_libdir}/pulse-%{apiver}/modules/module-match.so
%{_libdir}/pulse-%{apiver}/modules/module-mmkbd-evdev.so
%{_libdir}/pulse-%{apiver}/modules/module-native-protocol-fd.so
%{_libdir}/pulse-%{apiver}/modules/module-native-protocol-tcp.so
%{_libdir}/pulse-%{apiver}/modules/module-native-protocol-unix.so
%{_libdir}/pulse-%{apiver}/modules/module-null-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-oss.so
%{_libdir}/pulse-%{apiver}/modules/module-pipe-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-pipe-source.so
%{_libdir}/pulse-%{apiver}/modules/module-rescue-streams.so
%{_libdir}/pulse-%{apiver}/modules/module-rtp-recv.so
%{_libdir}/pulse-%{apiver}/modules/module-rtp-send.so
%{_libdir}/pulse-%{apiver}/modules/module-simple-protocol-tcp.so
%{_libdir}/pulse-%{apiver}/modules/module-simple-protocol-unix.so
%{_libdir}/pulse-%{apiver}/modules/module-sine.so
%{_libdir}/pulse-%{apiver}/modules/module-tunnel-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-tunnel-source.so
%{_libdir}/pulse-%{apiver}/modules/module-volume-restore.so
%{_libdir}/pulse-%{apiver}/modules/module-suspend-on-idle.so
%{_libdir}/pulse-%{apiver}/modules/module-default-device-restore.so
%{_libdir}/pulse-%{apiver}/modules/module-ladspa-sink.so
%{_libdir}/pulse-%{apiver}/modules/module-remap-sink.so


%files -n %{corelibname}
%defattr(-,root,root)
%{_libdir}/libpulsecore.so.%{coremajor}*


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libpulse.so.%{major}*
%{_libdir}/libpulse-simple.so.%{major}*


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
%{_libdir}/libpulsecore.so
%{_libdir}/libpulse-browse.so
%{_libdir}/libpulse-mainloop-glib.so
%{_libdir}/libpulse-simple.so
%dir %{_includedir}/pulse
%{_includedir}/pulse/*.h
%{_libdir}/pkgconfig/*.pc


%files esound-compat
%defattr(-,root,root)
%{_bindir}/esdcompat
%{_bindir}/esd


%files module-lirc
%defattr(-,root,root)
%{_libdir}/pulse-%{apiver}/modules/module-lirc.so


%files module-x11
%defattr(-,root,root)
%{_bindir}/pax11publish
%{_libdir}/pulse-%{apiver}/modules/libx11prop.so
%{_libdir}/pulse-%{apiver}/modules/libx11wrap.so
%{_libdir}/pulse-%{apiver}/modules/module-x11-bell.so
%{_libdir}/pulse-%{apiver}/modules/module-x11-publish.so
%{_libdir}/pulse-%{apiver}/modules/module-x11-xsmp.so
%config %{_sysconfdir}/xdg/autostart/pulseaudio-module-xsmp.desktop


%files module-zeroconf
%defattr(-,root,root)
%{_bindir}/pabrowse
%{_libdir}/pulse-%{apiver}/modules/libavahi-wrap.so
%{_libdir}/pulse-%{apiver}/modules/module-zeroconf-discover.so
%{_libdir}/pulse-%{apiver}/modules/module-zeroconf-publish.so


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
%{_bindir}/paplay
%{_bindir}/parec
%{_bindir}/pasuspender
# This is a is not a real shared library, it is used in LD_PRELOAD via padsp
%{_libdir}/libpulsedsp.so

