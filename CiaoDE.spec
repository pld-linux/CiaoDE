# TODO: finish emacs/xemacs
#
# Conditional build:
%bcond_with	emacs	# Emacs mode
%bcond_with	xemacs	# XEmacs mode
%bcond_without	java	# Java interface
#
Summary:	The Ciao Prolog development environment
Summary(pl.UTF-8):	Środowisko programistyczne Ciao Prolog
Name:		CiaoDE
Version:	1.14.2
Release:	0.1
License:	LGPL (Ciao), GPL (CiaoPP, lpdoc)
Group:		Development/Languages
Source0:	http://www.clip.dia.fi.upm.es/Software/Ciao/packages/branches/1.14/13646/%{name}-%{version}-13646.tar.gz
# Source0-md5:	11d0a41222314ae1be1b048a7888048e
Patch0:		%{name}-configure.patch
URL:		http://ciaohome.org/
BuildRequires:	gsl-devel
BuildRequires:	mysql-devel
Requires:	coreutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		mver	1.14
%define		emacs_sitestart_dir	%{_datadir}/emacs/site-lisp/site-start.d
# FIXME
%define		xemacs_sitestart_dir	%{_datadir}/xemacs-packages/lisp

%description
Ciao is next generation multi-paradigm programming environment with a
unique set of features:
 - A complete Prolog system, supporting ISO-Prolog.
 - Support for both restricting and extending the language.
 - Support for programming with functions, higher-order (with
   predicate abstractions), constraints, and objects, as well as
   feature terms (records), persistence, several control rules
   (breadth-first search, iterative deepening, ...), concurrency
   (threads/engines), a good base for distributed execution (agents),
   and parallel execution. Libraries also support WWW programming,
   sockets, external interfaces (C, Java, Tcl/Tk, relational
   databases, etc.), etc.
 - Support for programming in the large with a robust module/object
   system etc.
 - Support for programming in the small producing small executables
   (including only those builtins used by the program) and for writing
   scripts in Prolog.
And more.

%description -l pl.UTF-8
Ciao to wieloparadygmatowe środowisko programistyczne nowej generacji
o unikalnym połączeniu możliwości, m.in.:
 - Pełny system Prologu z obsługą ISO-Prologu.
 - Obsługa zarówno ograniczania, jak i rozszerzania języka.
 - Obsługa programowania z funkcjami, wyższego poziomu (z abstrakcją
   predykatów), ograniczeniami, obiektami, a także termami z cechami
   (rekordami), trwałością danych, różnymi regułami sterowania,
   współbieżnością (wątki/silniki), dobrą podstawą do wykonywania
   rozproszonego (agenci) oraz równoległego; biblioteki obsługują
   także programowanie WWW, gniazda, interfejsy zewnętrzne (C, Java,
   Tcl/Tk, relacyjne bazy danych itd.) itd.
 - Obsługą programowania w dużych środowiskach z potężnym systemem
   modułów/obiektów itd.
 - Obsługą programowania w małych środowiskach z tworzeniem małych
   programów wynikowych (zawierających tylko funkcje wbudowane użyte w
   programie) oraz pisania skryptów w Prologu.

%prep
%setup -q -n CiaoDE-%{version}-13646
%patch0 -p1

%build
./ciaosetup configure \
	--sysavail=all \
	--instype=ins \
	--prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--docdir=%{_docdir}/CiaoDE \
	--htmldir=%{_docdir}/CiaoDE/html \
	--cflags="%{rpmcflags}" \
	--ldflags="%{rpmldflags}" \
	--stop_if_error=yes \
	--update_bashrc=no \
	--update_cshrc=no \
	--update_dotemacs=no \
	--update_dotxemasc=no \
%if %{with emacs}
	--install_emacs_support=yes \
	--ciaomodeinitdir=%{emacs_sitestart_dir} \
	--emacsinitfile=ciao-mode-init.el \
%else
	--install_emacs_support=no \
%endif
%if %{with xemacs}
	--install_xemacs_support=yes \
	--xemacsinitdir=%{xemacs_sitestart_dir} \
	--xemacsinitfile=ciao-mode-init.el \
%else
	--install_xemacs_support=no \
%endif
	--with_gsl=yes \
	--with_mysql=yes \
	%{?with_java:--with_java_interface=yes}

./ciaosetup build

%install
rm -rf $RPM_BUILD_ROOT

BUILD_ROOT=$RPM_BUILD_ROOT \
./ciaosetup install

# sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ciao/ciao-%{mver}/library/{apll,concurrency,random,sha1,sockets}/*.[cho]
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ciao/ciao-%{mver}/library/{apll,concurrency,random,sockets}/Makefile

install -d $RPM_BUILD_ROOT/etc/profile.d
mv $RPM_BUILD_ROOT%{_libdir}/ciao/ciao-%{mver}/DOTprofile $RPM_BUILD_ROOT/etc/profile.d/ciao.sh
mv $RPM_BUILD_ROOT%{_libdir}/ciao/ciao-%{mver}/DOTcshrc $RPM_BUILD_ROOT/etc/profile.d/ciao.csh
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ciao/DOT*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/checkline*
%attr(755,root,root) %{_bindir}/ciao*
%attr(755,root,root) %{_bindir}/cleandirs*
%attr(755,root,root) %{_bindir}/compiler_output*
%attr(755,root,root) %{_bindir}/fileinfo*
%attr(755,root,root) %{_bindir}/get_deps*
%attr(755,root,root) %{_bindir}/lpdoc*
%attr(755,root,root) %{_bindir}/lpmake*
%attr(755,root,root) %{_bindir}/pldiff*
%attr(755,root,root) %{_bindir}/plindent*
%attr(755,root,root) %{_bindir}/prolog
%attr(755,root,root) %{_bindir}/show_asr*
%attr(755,root,root) %{_bindir}/show_deps*
%attr(755,root,root) %{_bindir}/synch_actions*
%attr(755,root,root) %{_bindir}/viewpo*
%attr(755,root,root) /etc/profile.d/ciao.csh
%attr(755,root,root) /etc/profile.d/ciao.sh
%dir %{_libdir}/ciao
%dir %{_libdir}/ciao/ciao-%{mver}
%{_libdir}/ciao/ciao-%{mver}/contrib
%dir %{_libdir}/ciao/ciao-%{mver}/engine
%attr(755,root,root) %{_libdir}/ciao/ciao-%{mver}/engine/ciaoengine*
%{_libdir}/ciao/ciao-%{mver}/examples
%{_libdir}/ciao/ciao-%{mver}/include
%{_libdir}/ciao/ciao-%{mver}/lib
%dir %{_libdir}/ciao/ciao-%{mver}/library
%{_libdir}/ciao/ciao-%{mver}/library/NOCOMPILEFILES
%{_libdir}/ciao/ciao-%{mver}/library/*.asr
%{_libdir}/ciao/ciao-%{mver}/library/*.itf
%{_libdir}/ciao/ciao-%{mver}/library/*.pl
%{_libdir}/ciao/ciao-%{mver}/library/*.po
# junk???
%{_libdir}/ciao/ciao-%{mver}/library/davinci8Wznpg
%{_libdir}/ciao/ciao-%{mver}/library/davinciQNZdYP
%{_libdir}/ciao/ciao-%{mver}/library/actmods
%{_libdir}/ciao/ciao-%{mver}/library/agent
%{_libdir}/ciao/ciao-%{mver}/library/andorra
%{_libdir}/ciao/ciao-%{mver}/library/andprolog
%{_libdir}/ciao/ciao-%{mver}/library/andprolog_old
%dir %{_libdir}/ciao/ciao-%{mver}/library/apll
%{_libdir}/ciao/ciao-%{mver}/library/apll/*.asr
%{_libdir}/ciao/ciao-%{mver}/library/apll/*.itf
%{_libdir}/ciao/ciao-%{mver}/library/apll/*.pl
%{_libdir}/ciao/ciao-%{mver}/library/apll/*.po
%{_libdir}/ciao/ciao-%{mver}/library/apll/*_LINUX*.so
%{_libdir}/ciao/ciao-%{mver}/library/argnames
%{_libdir}/ciao/ciao-%{mver}/library/benchmarks
%{_libdir}/ciao/ciao-%{mver}/library/bf
%{_libdir}/ciao/ciao-%{mver}/library/byrdbox
%{_libdir}/ciao/ciao-%{mver}/library/chr
%{_libdir}/ciao/ciao-%{mver}/library/class
%{_libdir}/ciao/ciao-%{mver}/library/clpq
%{_libdir}/ciao/ciao-%{mver}/library/clpqr-common
%{_libdir}/ciao/ciao-%{mver}/library/clpr
%dir %{_libdir}/ciao/ciao-%{mver}/library/concurrency
%{_libdir}/ciao/ciao-%{mver}/library/concurrency/*.asr
%{_libdir}/ciao/ciao-%{mver}/library/concurrency/*.itf
%{_libdir}/ciao/ciao-%{mver}/library/concurrency/*.pl
%{_libdir}/ciao/ciao-%{mver}/library/concurrency/*.po
%attr(755,root,root) %{_libdir}/ciao/ciao-%{mver}/library/concurrency/*_LINUX*.so
%{_libdir}/ciao/ciao-%{mver}/library/concurrency/examples
%{_libdir}/ciao/ciao-%{mver}/library/det_hook
%{_libdir}/ciao/ciao-%{mver}/library/dialect
%{_libdir}/ciao/ciao-%{mver}/library/emacs
%{_libdir}/ciao/ciao-%{mver}/library/expander
%{_libdir}/ciao/ciao-%{mver}/library/factsdb
%{_libdir}/ciao/ciao-%{mver}/library/fake
%{_libdir}/ciao/ciao-%{mver}/library/fdtypes
%{_libdir}/ciao/ciao-%{mver}/library/file_locks
%{_libdir}/ciao/ciao-%{mver}/library/freeze
%{_libdir}/ciao/ciao-%{mver}/library/fsyntax
%{_libdir}/ciao/ciao-%{mver}/library/fuzzy
%{_libdir}/ciao/ciao-%{mver}/library/graphs
%{_libdir}/ciao/ciao-%{mver}/library/id
%{_libdir}/ciao/ciao-%{mver}/library/indexer
%{_libdir}/ciao/ciao-%{mver}/library/interface
%{_libdir}/ciao/ciao-%{mver}/library/javall
%{_libdir}/ciao/ciao-%{mver}/library/librowser
%{_libdir}/ciao/ciao-%{mver}/library/lpsettings_based_app
%{_libdir}/ciao/ciao-%{mver}/library/make
%{_libdir}/ciao/ciao-%{mver}/library/menu
%{_libdir}/ciao/ciao-%{mver}/library/netscape
%{_libdir}/ciao/ciao-%{mver}/library/objects
%{_libdir}/ciao/ciao-%{mver}/library/persdb
%{_libdir}/ciao/ciao-%{mver}/library/persdb_mysql
%{_libdir}/ciao/ciao-%{mver}/library/persdb_sql_common
%{_libdir}/ciao/ciao-%{mver}/library/pillow
%dir %{_libdir}/ciao/ciao-%{mver}/library/random
%{_libdir}/ciao/ciao-%{mver}/library/random/*.asr
%{_libdir}/ciao/ciao-%{mver}/library/random/*.itf
%{_libdir}/ciao/ciao-%{mver}/library/random/*.pl
%{_libdir}/ciao/ciao-%{mver}/library/random/*.po
%attr(755,root,root) %{_libdir}/ciao/ciao-%{mver}/library/random/*_LINUX*.so
%dir %{_libdir}/ciao/ciao-%{mver}/library/sha1
%{_libdir}/ciao/ciao-%{mver}/library/sha1/*.asr
%{_libdir}/ciao/ciao-%{mver}/library/sha1/*.itf
%{_libdir}/ciao/ciao-%{mver}/library/sha1/*.pl
%{_libdir}/ciao/ciao-%{mver}/library/sha1/*.po
%attr(755,root,root) %{_libdir}/ciao/ciao-%{mver}/library/sha1/*_LINUX*.so
%{_libdir}/ciao/ciao-%{mver}/library/sha1/examples
%{_libdir}/ciao/ciao-%{mver}/library/show_trans
%dir %{_libdir}/ciao/ciao-%{mver}/library/sockets
%{_libdir}/ciao/ciao-%{mver}/library/sockets/*.asr
%{_libdir}/ciao/ciao-%{mver}/library/sockets/*.itf
%{_libdir}/ciao/ciao-%{mver}/library/sockets/*.pl
%{_libdir}/ciao/ciao-%{mver}/library/sockets/*.po
%attr(755,root,root) %{_libdir}/ciao/ciao-%{mver}/library/sockets/*_LINUX*.so
%{_libdir}/ciao/ciao-%{mver}/library/sockets/examples
%{_libdir}/ciao/ciao-%{mver}/library/symfnames
%{_libdir}/ciao/ciao-%{mver}/library/tcltk
%{_libdir}/ciao/ciao-%{mver}/library/toplevel
%{_libdir}/ciao/ciao-%{mver}/library/tracing
%{_libdir}/ciao/ciao-%{mver}/library/when
%{_libdir}/ciao/ciao-%{mver}/library/xrefs
%{_includedir}/ciao_prolog.h
