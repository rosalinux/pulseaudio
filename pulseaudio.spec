%define name pulseaudio
%define version 0.9.7
%define rel 1
%define svn 1989
%if %{svn}
%define release %mkrel 0.%{svn}.%rel
%else
%define release %mkrel %rel
%endif

%define major 0
%define coremajor 4
%define apiver 0.9

%define libname %mklibname %name %major
%define libname_devel %mklibname -d %name
%define corelibname %mklibname pulsecore %coremajor

Summary: Sound server for Linux
Name: %{name}
Version: %{version}
Release: %{release}
%if %{svn}
Source0: %{name}-%{svn}.tar.bz2
%else
Source0: %{name}-%{version}.tar.bz2
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
#BuildRequires: libasyncns-devel
Provides: polypaudio
Obsoletes: polypaudio

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

%package -n %corelibname
Summary: Shared library part of the polpyaudio sound server
Group: System/Libraries

%description -n %corelibname
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

This contains the shared library needed by pulseaudio based applications.

%package -n %libname
Summary: Shared library part of the pulseaudio sound server
Group: System/Libraries

%description -n %libname
Pulseaudio is a sound server for Linux and other Unix like operating
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

This contains the shared library needed by pulseaudio based applications.

%package -n %libname_devel
Summary: Development headers of the pulseaudio sound server
Group: Development/C
Requires: %corelibname = %version-%release
Requires: %libname = %version-%release
Provides: lib%name-devel = %version-%release
Provides: %name-devel = %version-%release
Obsoletes: %mklibname -d %name %major

%description -n %libname_devel
Pulseaudio is a sound server for Linux and other Unix like operating
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

This contains the C headers and libraries needed to build pulseaudio
based applications.


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
%else
export CPPFLAGS=-I%_includedir/alsa
%endif
%configure2_5x --disable-glib1
make
make doxygen

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig
%post -n %corelibname -p /sbin/ldconfig
%postun -n %corelibname -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README doxygen/html
%attr(4755,root,root) %_bindir/%name
%_bindir/esdcompat
%_bindir/pabrowse
%_bindir/pacat
%_bindir/pacmd
%_bindir/pactl
%_bindir/padsp
%_bindir/paplay
%_bindir/parec
%_bindir/pasuspender
%_bindir/pax11publish
%dir %_libdir/pulse
%_libdir/pulse/gconf-helper
%dir %_sysconfdir/pulse
%config(noreplace) %_sysconfdir/pulse/client.conf
%config(noreplace) %_sysconfdir/pulse/daemon.conf
%config(noreplace) %_sysconfdir/pulse/default.pa
%_sysconfdir/xdg/autostart/%name-module-xsmp.desktop

%files -n %corelibname
%defattr(-,root,root)
%_libdir/libpulsecore.so.%{coremajor}*

%files -n %libname
%defattr(-,root,root)
%_libdir/libpulsedsp.so
%_libdir/libpulse.so.%{major}*
%_libdir/libpulse-browse.so.%{major}*
%_libdir/libpulse-mainloop-glib.so.%{major}*
%_libdir/libpulse-simple.so.%{major}*
%dir %_libdir/pulse-%apiver
%dir %_libdir/pulse-%apiver/modules
%_libdir/pulse-%apiver/modules/*.so
%attr(644,root,root) %_libdir/pulse-%apiver/modules/*.la

%files -n %libname_devel
%defattr(-,root,root)
%attr(644,root,root) %_libdir/lib*.la
%_libdir/lib*.a
%_libdir/libpulse.so
%_libdir/libpulsecore.so
%_libdir/libpulse-browse.so
%_libdir/libpulse-mainloop-glib.so
%_libdir/libpulse-simple.so
%dir %_includedir/pulse
%_includedir/pulse/*.h
%_libdir/pkgconfig/*.pc
