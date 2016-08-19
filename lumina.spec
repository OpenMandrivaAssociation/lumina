%define debug_package %{nil}

Name: lumina
Version: 1.0.0
Release: 1
# Packaged directly from their git tree at
# http://github.com/trueos/lumina.git
# (the build will fail without .git/ packaged!)
Source0: %{name}-%{version}.tar.xz
Source1: https://github.com/trueos/lumina-i18n/archive/v%{version}-Release.tar.gz
Patch0: lumina-1.0.0-defaults.patch
Summary: The Lumina Desktop Environment
URL: http://lumina-desktop.org/
License: BSD
Group: Graphical desktop/KDE
BuildRequires: qmake5
BuildRequires: git-core
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5Concurrent)
BuildRequires: cmake(Qt5Gui)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5Svg)
BuildRequires: cmake(Qt5Multimedia)
BuildRequires: cmake(Qt5MultimediaWidgets)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5X11Extras)
BuildRequires: pkgconfig(xcb-ewmh)
BuildRequires: pkgconfig(xcb-atom)
BuildRequires: pkgconfig(xcb-image)

# Desktop requirements
Requires: %{name}-open = %{EVRD}
Requires: %{name}-config = %{EVRD}
Requires: %{name}-fm = %{EVRD}
Requires: %{name}-screenshot = %{EVRD}
Requires: %{name}-search = %{EVRD}
Requires: %{name}-info = %{EVRD}
Requires: %{name}-textedit = %{EVRD}
Requires: %{name}-xconfig = %{EVRD}
Requires: %{name}-fileinfo = %{EVRD}
# FIXME is this configurable?
Requires: fluxbox

Suggests: qupzilla
Suggests: kmail

%libpackage LuminaUtils 1
%define devpkg %{mklibname -d LuminaUtils}

%description
The Lumina Desktop Environment is a lightweight system interface designed
for use on any Unix-like operating system. Lumina is based on using
plugins, which allows the entire interface to be arranged by each individual
user as desired.
A system wide default layout is also included, and is configurable by the
system administrator.
This allows every system (or user session) to be designed to maximize the
individual user's productivity.

The Lumina desktop developers understand that the point of a computer
system is to run applications, so Lumina was designed to require as few
system dependencies/requirements as possible. This allows it to be used
to revitalize older systems or to allow the user to run applications that
may need a higher percentage of the system resources than were previously
available with other desktop environments.

All of this results in a very lightweight, customizable, and smooth desktop
experience with minimal system overhead.

%package -n %{devpkg}
Summary:            Development libraries for Lumina Desktop
Group:              Development/C++

%description -n %{devpkg}
This package provides the files needed to develop plugins
or extensions for the Lumina Desktop Environment, or
to develop applications that use Lumina Desktop libraries.

%package open
Summary:            xdg-open style utility for Lumina Desktop
Group:              Graphical desktop/KDE

%description open
This package provides lumina-open, which handles opening of
files and URLs according to the system-wide mimetype association.
It also provides an optional selector if more than one application
is assigned with the given url or file type.

%package config
Summary:            Configuration utility for Lumina Desktop
Group:              Graphical desktop/KDE

%description config
This package provides lumina-config, which allows changing
various aspects of lumina and fluxbox, like the wallpaper being
used, theme, icons, panel (and plugins), startup and default
applications, desktop menu and more.

%package fm
Summary:            File manager for Lumina Desktop
Group:              Graphical desktop/KDE

%description fm
This package provides lumina-fm, which is a simple file manager
with support for multiple view modes, tabbed browsing,
including an integrated slideshow-based picture viewer.

%package screenshot
Summary:            Screenshot utility for Lumina Desktop
Group:              Graphical desktop/KDE

%description screenshot
This package provides lumina-screenshot, which is a simple
screenshot utility that allows to snapshot the whole desktop
or a single window after a configurable delay.

Optionally the window border can be hidden when taking a
screenshot of a single window.


%package search
Summary:            Search utility for Lumina Desktop
Group:              Graphical desktop/KDE

%description search
This package provides lumina-search, which is a simple
search utility that allows to search for applications or
files and directories in the home directory and launch
or open them.


%package info
Summary:            Basic information utility for Lumina Desktop
Group:              Graphical desktop/KDE

%description info
This package provides lumina-info, which is a simple
utility that displays various information about the Lumina
installation, like paths, contributors, license or version.

%package textedit
Summary:            Text editor for Lumina Desktop
Group:              Graphical desktop/KDE

%description textedit
This package provides lumina-textedit, which is a simple
text editor meant for use with the Lumina desktop

%package xconfig
Summary:            X server display configuration tool for Lumina Desktop
Group:              Graphical desktop/KDE

%description xconfig
This package provides lumina-xconfig, which is a simple
multi-head aware display configuration tool for configuring
the X server.


%package fileinfo
Summary:            Desktop file editor for Lumina Desktop
Group:              Graphical desktop/KDE

%description fileinfo
This package provides lumina-fileinfo, which is an
advanced desktop file (menu) editor.

%prep
%setup -qn lumina -a 1
%apply_patches
qmake-qt5 CONFIG+=configure PREFIX=%{_prefix} LIBPREFIX=%{_libdir} L_LIBDIR=%{_libdir} L_ETCDIR=%{_sysconfdir}

%build
%make

%install
%make install INSTALL_ROOT="%{buildroot}"
SRC="`pwd`"
cd "%{buildroot}"%{_datadir}/lumina-desktop
mkdir i18n
cd i18n
tar xf $SRC/lumina-i18n*/dist/lumina-i18n.txz
for i in *.qm; do
	F="`echo $i |cut -d_ -f1`"
	L="`echo $i |cut -d_ -f2- |cut -d. -f1`"
	echo "%lang($L) %%{_datadir}/lumina-desktop/i18n/$i" >>$SRC/$F.lang
done

%files -n %{devpkg}
%{_libdir}/libLuminaUtils.so
%{_includedir}/LuminaXDG.h
%{_includedir}/LuminaUtils.h
%{_includedir}/LuminaX11.h
%{_includedir}/LuminaThemes.h
%{_includedir}/LuminaOS.h
%{_includedir}/LuminaSingleApplication.h

%files -f lumina-desktop.lang
%{_bindir}/lumina-desktop
%{_bindir}/start-lumina-desktop
%{_sysconfdir}/luminaDesktop.conf.dist
%{_datadir}/pixmaps/Lumina-DE.png
%{_datadir}/xsessions/Lumina-DE.desktop
%dir %{_datadir}/lumina-desktop
%{_datadir}/lumina-desktop/compton.conf
%{_datadir}/lumina-desktop/desktop-background.jpg
%{_datadir}/lumina-desktop/luminaDesktop.conf
%{_datadir}/lumina-desktop/fluxbox-init-rc
%{_datadir}/lumina-desktop/fluxbox-keys
%{_datadir}/lumina-desktop/Login.ogg
%{_datadir}/lumina-desktop/Logout.ogg
%dir %{_datadir}/lumina-desktop/colors
%{_datadir}/lumina-desktop/colors/Lumina-Red.qss.colors
%{_datadir}/lumina-desktop/colors/Lumina-Green.qss.colors
%{_datadir}/lumina-desktop/colors/Lumina-Purple.qss.colors
%{_datadir}/lumina-desktop/colors/Lumina-Gold.qss.colors
%{_datadir}/lumina-desktop/colors/Lumina-Glass.qss.colors
%{_datadir}/lumina-desktop/colors/PCBSD10-Default.qss.colors
%{_datadir}/lumina-desktop/colors/Black.qss.colors
%{_datadir}/lumina-desktop/colors/Blue-Light.qss.colors
%{_datadir}/lumina-desktop/colors/Grey-Dark.qss.colors
%{_datadir}/lumina-desktop/colors/Solarized-Dark.qss.colors
%{_datadir}/lumina-desktop/colors/Solarized-Light.qss.colors
%dir %{_datadir}/lumina-desktop/themes
%{_datadir}/lumina-desktop/themes/Lumina-default.qss.template
%{_datadir}/lumina-desktop/themes/Glass.qss.template
%{_datadir}/lumina-desktop/themes/None.qss.template
%dir %{_datadir}/lumina-desktop/menu-scripts
%{_datadir}/lumina-desktop/menu-scripts/ls.json.sh
%dir %{_datadir}/wallpapers/Lumina-DE
%{_datadir}/wallpapers/Lumina-DE/Lumina_Wispy_blue-grey.jpg
%{_datadir}/wallpapers/Lumina-DE/Lumina_Wispy_blue-grey-zoom.jpg
%{_datadir}/wallpapers/Lumina-DE/Lumina_Wispy_grey-blue.jpg
%{_datadir}/wallpapers/Lumina-DE/Lumina_Wispy_grey-blue-zoom.jpg
%{_datadir}/wallpapers/Lumina-DE/Lumina_Wispy_gold.jpg
%{_datadir}/wallpapers/Lumina-DE/Lumina_Wispy_green.jpg
%{_datadir}/wallpapers/Lumina-DE/Lumina_Wispy_purple.jpg
%{_datadir}/wallpapers/Lumina-DE/Lumina_Wispy_red.jpg
%{_datadir}/applications/lumina-support.desktop
%dir %{_datadir}/lumina-desktop/i18n

%files open -f lumina-open.lang
%{_bindir}/lumina-open

%files config -f lumina-config.lang
%{_bindir}/lumina-config
%{_datadir}/applications/lumina-config.desktop

%files fm -f lumina-fm.lang
%{_bindir}/lumina-fm
%{_datadir}/pixmaps/Insight-FileManager.png
%{_datadir}/applications/lumina-fm.desktop

%files screenshot -f lumina-screenshot.lang
%{_bindir}/lumina-screenshot
%{_datadir}/applications/lumina-screenshot.desktop

%files search -f lumina-search.lang
%{_bindir}/lumina-search
%{_datadir}/applications/lumina-search.desktop

%files info -f lumina-info.lang
%{_bindir}/lumina-info
%{_datadir}/applications/lumina-info.desktop

%files textedit -f lumina-textedit.lang
%{_bindir}/lte
%{_bindir}/lumina-textedit
%{_datadir}/applications/lumina-textedit.desktop

%files xconfig -f lumina-xconfig.lang
%{_bindir}/lumina-xconfig
%{_datadir}/applications/lumina-xconfig.desktop

%files fileinfo -f lumina-fileinfo.lang
%{_bindir}/lumina-fileinfo
%{_datadir}/applications/lumina-fileinfo.desktop
