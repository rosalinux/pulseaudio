%define name pulseaudio
%define version 0.9.5
%define svn 1437
%if %{svn}
%define release %mkrel 1.%{svn}.1
%else
%define release %mkrel 1
%endif
%define major 0
%define coremajor 2
%define apiver 0.9
%define libname %mklibname %name %major
%define corelibname %mklibname pulsecore %coremajor

Summary: Sound server for Linux
Name: %{name}
Version: %{version}
Release: %{release}
%if %{svn}
Source0: %{name}-%{version}-%{svn}.tar.bz2
%else
Source0: %{name}-%{version}.tar.bz2
%endif
Patch0:  pulseaudio-0.9.5-use-master.patch
Patch1:  pulseaudio-0.9.5-r1437-hal-log-fix.patch
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
Summary: Shared library part of the polpyaudio sound server
Group: System/Libraries

%description -n %libname
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

%package -n %libname-devel
Summary: Development headers of the polpyaudio sound server
Group: Development/C
Requires: %corelibname = %version
Requires: %libname = %version
Provides: lib%name-devel = %version-%release

%description -n %libname-devel
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

This contains the C headers and libraries needed to build pulseaudio
based applications.


%prep
%setup -q
%patch0 -p0 -b .use-master
%patch1 -p0 -b .hal-log

%build
%if %{svn}
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
%_bindir/pax11publish
%_libdir/pulse/
%dir %_sysconfdir/pulse
%config(noreplace) %_sysconfdir/pulse/client.conf
%config(noreplace) %_sysconfdir/pulse/daemon.conf
%config(noreplace) %_sysconfdir/pulse/default.pa

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
%dir %_libdir/pulse-%apiver/
%dir %_libdir/pulse-%apiver/modules
%_libdir/pulse-%apiver/modules/*.so
%attr(644,root,root) %_libdir/pulse-%apiver/modules/*.la

%files -n %libname-devel
%defattr(-,root,root)
%attr(644,root,root) %_libdir/lib*.la
%_libdir/lib*.a
%_libdir/libpulse.so
%_libdir/libpulsecore.so
%_libdir/libpulse-browse.so
%_libdir/libpulse-mainloop-glib.so
%_libdir/libpulse-simple.so
%_includedir/pulse/
%_includedir/pulsecore/
%_libdir/pkgconfig/*.pc
