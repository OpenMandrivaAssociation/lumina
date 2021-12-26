%define debug_package %{nil}
%define ver 1.6.2
%define patchlevel %{nil}

Name: lumina
Version: %{ver}%{?patchlevel:p%{patchlevel}}
Release: 1
%if "%{patchlevel}" != ""
Source0: https://github.com/trueos/lumina/archive/v%{ver}%{?patchlevel:-p%{patchlevel}}.tar.gz
%else
Source0: https://github.com/trueos/lumina/archive/v%{ver}/%{name}-%{ver}.tar.gz
%endif
Patch0: lumina-1.0.0-defaults.patch
Patch1: lumina-1.1.0p1-no-isystem-usr-include.patch
# issue https://github.com/lumina-desktop/lumina/issues/771
Patch2: lumina-1.6.1-fix-install-checkpass.patch
Summary: The Lumina Desktop Environment
URL: http://lumina-desktop.org/
License: BSD
Group: Graphical desktop/KDE
BuildRequires: qmake5
BuildRequires: git-core
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5Concurrent)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Gui)
BuildRequires: cmake(Qt5LinguistTools)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5PrintSupport)
BuildRequires: cmake(Qt5Svg)
BuildRequires: cmake(Qt5Quick)
BuildRequires: cmake(Qt5Xml)
BuildRequires: %{_lib}qt5themesupport-static-devel
BuildRequires: cmake(Qt5Multimedia)
BuildRequires: cmake(Qt5MultimediaWidgets)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5X11Extras)
BuildRequires: pkgconfig(pam)
BuildRequires: pkgconfig(xcb-ewmh)
BuildRequires: pkgconfig(xcb-atom)
BuildRequires: pkgconfig(xcb-image)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xdamage)
BuildRequires: pkgconfig(poppler-qt5)
Obsoletes: %{mklibname LuminaUtils 1} < %{EVRD}
Obsoletes: %{mklibname -d LuminaUtils} < %{EVRD}

# Desktop requirements
Requires: %{name}-open = %{EVRD}
Requires: %{name}-archiver = %{EVRD}
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

Requires: la-capitaine-icon-theme

Recommends: falkon
Recommends: kmail

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

%package archiver
Summary:            Graphical archiver for the Lumina Desktop
Group:              Graphical desktop/KDE

%description archiver
This package provides lumina-archiver, which handles opening of
tar and zip files

%package photo
Summary:            Photo viewer for the Lumina Desktop
Group:              Graphical desktop/KDE

%description photo
This package provides lumina-photo, a photo viewer for the
Lumina Desktop.

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

%package mediaplayer
Summary:            Media player for Lumina Desktop
Group:              Graphical desktop/KDE
Suggests:           pianobar

%description mediaplayer
This package provides lumina-mediaplayer, which is a simple
media player.

%prep
%if "%{patchlevel}" != ""
%setup -qn lumina-%{ver}%{?patchlevel:-p%{patchlevel}}
%else
%setup -qn lumina-%{ver}
%endif
%patch0 -p1
%patch1 -p1
%patch2 -p0

# The "fur" locale is broken (only empty translations) and not known by glibc
# Let's kill it for now
find . -name "*_fur.*" |xargs rm

qmake-qt5 CONFIG+=configure CONFIG+=WITH_I18N PREFIX=%{_prefix} LIBPREFIX=%{_libdir} L_LIBDIR=%{_libdir} L_ETCDIR=%{_sysconfdir}

%build
%make_build

%install
%make_install INSTALL_ROOT="%{buildroot}"

[ "%{_mandir}" != "%{_prefix}/man" ] && mv %{buildroot}%{_prefix}/man %{buildroot}%{_mandir}

for i in l-archiver l-fileinfo l-mediap l-photo l-screenshot l-te lumina-config lumina-desktop lumina-fm lumina-info lumina-open lumina-search lumina-xconfig; do
	%find_lang $i --with-qt
done

%files -f lumina-desktop.lang
%{_bindir}/lumina-desktop
%{_bindir}/lumina-pingcursor
%{_bindir}/lumina-sudo
%{_bindir}/start-lumina-desktop
%{_mandir}/man8/start-lumina-desktop.8*
%{_sysconfdir}/luminaDesktop.conf.dist
%{_datadir}/xsessions/Lumina-DE.desktop
%{_datadir}/icons/lumina-icons
%dir %{_datadir}/lumina-desktop
%{_datadir}/lumina-desktop/compton.conf
%{_datadir}/lumina-desktop/desktop-background.jpg
%{_datadir}/lumina-desktop/luminaDesktop.conf
%{_datadir}/lumina-desktop/fluxbox-init-rc
%{_datadir}/lumina-desktop/fluxbox-keys
%{_datadir}/lumina-desktop/Login.ogg
%{_datadir}/lumina-desktop/Logout.ogg
%{_datadir}/lumina-desktop/globs2
%{_datadir}/lumina-desktop/low-battery.ogg
%dir %{_datadir}/lumina-desktop/themes
%{_datadir}/lumina-desktop/themes/Lumina-default.qss.template
%{_datadir}/lumina-desktop/themes/Glass.qss.template
%{_datadir}/lumina-desktop/themes/None.qss.template
%{_datadir}/lumina-desktop/themes/DarkGlass.qss.template
%dir %{_datadir}/lumina-desktop/menu-scripts
%{_datadir}/lumina-desktop/menu-scripts/ls.json.sh
%{_datadir}/lumina-desktop/menu-scripts/README.md
%{_datadir}/lumina-desktop/Lumina-DE.png
%dir %{_datadir}/lumina-desktop/i18n
%{_datadir}/lumina-desktop/screensavers
%{_datadir}/lumina-desktop/theme.cfg
%{_datadir}/applications/lumina-support.desktop
#dir #{_datadir}/lumina-desktop/i18n
%{_datadir}/icons/material-design-dark
%{_datadir}/icons/material-design-light
#{_datadir}/icons/hicolor/scalable/apps/Lumina-DE.png
%{_mandir}/man1/lumina-desktop.1*
# Should this be separate? It's not strictly required...
%{_bindir}/lthemeengine
%{_bindir}/lthemeengine-sstest
%{_libdir}/qt5/plugins/platformthemes/liblthemeengine.so
%{_libdir}/qt5/plugins/styles/liblthemeengine-style.so
%{_datadir}/applications/lthemeengine.desktop
%{_datadir}/lthemeengine
%{_datadir}/pixmaps/Lumina-DE.svg

%files archiver -f l-archiver.lang
%{_bindir}/lumina-archiver
%{_datadir}/applications/lumina-archiver.desktop
%{_mandir}/man1/lumina-archiver.1*

%files open -f lumina-open.lang
%{_bindir}/lumina-open
%{_mandir}/man1/lumina-open.1*

%files config -f lumina-config.lang
%{_bindir}/lumina-config
%{_datadir}/applications/lumina-config.desktop
%{_mandir}/man1/lumina-config.1*

%files fm -f lumina-fm.lang
%{_bindir}/lumina-fm
%{_datadir}/applications/lumina-fm.desktop
#{_datadir}/icons/hicolor/scalable/apps/Insight-FileManager.png
%{_mandir}/man1/lumina-fm.1*
%{_datadir}/pixmaps/Insight-FileManager.svg

%files mediaplayer -f l-mediap.lang
%{_bindir}/lumina-mediaplayer
%{_datadir}/applications/lumina-mediaplayer.desktop
%{_datadir}/applications/lumina-mediaplayer-pandora.desktop
%{_mandir}/man1/lumina-mediaplayer.1*

%files screenshot -f l-screenshot.lang
%{_bindir}/lumina-screenshot
%{_datadir}/applications/lumina-screenshot.desktop
%{_mandir}/man1/lumina-screenshot.1*

%files search -f lumina-search.lang
%{_bindir}/lumina-search
%{_datadir}/applications/lumina-search.desktop
%{_mandir}/man1/lumina-search.1*

%files info -f lumina-info.lang
%{_bindir}/lumina-info
%{_datadir}/applications/lumina-info.desktop
%{_mandir}/man1/lumina-info.1*

%files textedit -f l-te.lang
%{_bindir}/lte
%{_bindir}/lumina-textedit
%{_datadir}/applications/lumina-textedit.desktop
%{_datadir}/lumina-desktop/syntax_rules
%{_mandir}/man1/lumina-textedit.1*

%files xconfig -f lumina-xconfig.lang
%{_bindir}/lumina-xconfig
%{_datadir}/applications/lumina-xconfig.desktop
%{_mandir}/man1/lumina-xconfig.1*

%files fileinfo -f l-fileinfo.lang
%{_bindir}/lumina-fileinfo
%{_datadir}/applications/lumina-fileinfo.desktop
%{_mandir}/man1/lumina-fileinfo.1*

%files photo -f l-photo.lang
%{_bindir}/lumina-photo
%{_datadir}/applications/lumina-photo.desktop
%{_mandir}/man1/lumina-photo.1.*
