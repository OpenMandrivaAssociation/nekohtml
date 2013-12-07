Summary:	HTML scanner and tag balancer
Name:		nekohtml
Version:	1.9.18
Release:	3
License:	Apache License
Group:		Development/Java
Url:		http://nekohtml.sourceforge.net/
Source0:	http://garr.dl.sourceforge.net/project/nekohtml/nekohtml/nekohtml-%{version}/nekohtml-%{version}.tar.gz
# Source 1      http://www.jpackage.org/cgi-bin/viewvc.cgi/*checkout*/rpms/devel/nekohtml/nekohtml-filter.sh?root=jpackage&content-type=text%2Fplain
Source1:	%{name}-filter.sh
Patch0:		%{name}-crosslink.patch
Patch1:		%{name}-1.9.6-jars.patch
BuildArch:	noarch
BuildRequires:	java-1.6.0-openjdk-devel
BuildRequires:	java-rpmbuild >= 0:1.6
BuildRequires:	ant
BuildRequires:	java-javadoc
BuildRequires:	bcel-javadoc
BuildRequires:	xerces-j2 >= 0:2.7.1
BuildRequires:	xerces-j2-javadoc-xni
BuildRequires:	xerces-j2-javadoc-impl
Requires:	bcel
Requires:	jpackage-utils >= 0:1.6
Requires:	xerces-j2 >= 0:2.7.1

%description
NekoHTML is a simple HTML scanner and tag balancer that enables
application programmers to parse HTML documents and access the
information using standard XML interfaces. The parser can scan HTML
files and "fix up" many common mistakes that human (and computer)
authors make in writing HTML documents.  NekoHTML adds missing parent
elements; automatically closes elements with optional end tags; and
can handle mismatched inline element tags.
NekoHTML is written using the Xerces Native Interface (XNI) that is
the foundation of the Xerces2 implementation. This enables you to use
the NekoHTML parser with existing XNI tools without modification or
rewriting code.

%package        javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java
Requires:	jpackage-utils >= 0:1.6
Requires(postun):	jpackage-utils >= 0:1.6

%description    javadoc
Javadoc for %{name}.

%package        demo
Summary:	Demo for %{name}
Group:		Development/Java
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	jpackage-utils >= 0:1.6
Requires(postun):	jpackage-utils >= 0:1.6

%description    demo
Demonstrations and samples for %{name}.

%track
prog %{name} = {
	url = http://sourceforge.net/projects/nekohtml/files/
	regex = "Download nekohtml-(__VER__)\.tar\.gz
	version = %{version}
}

%prep
%setup -q
%apply_patches
%{_bindir}/find . -name "*.jar" | %{_bindir}/xargs -t %{__rm}
perl -pi -e 's/\r$//g' *.txt doc/*.html
rm -r doc/javadoc

%build
export CLASSPATH=$(build-classpath bcel xerces-j2)
export OPT_JAR_LIST=:
export JAVA_HOME=%_prefix/lib/jvm/java-1.6.0
ant \
    -Dbuild.sysclasspath=first \
    -Djava.dir=%{_javadir} \
    -Djar.file=%{name}-%{version}.jar \
    -Djar.xni.file=%{name}-xni-%{version}.jar \
    -Djar.samples.file=%{name}-samples-%{version}.jar \
    -Dbcel.javadoc=%{_javadocdir}/bcel \
    -Dj2se.javadoc=%{_javadocdir}/java \
    -Dxni.javadoc=%{_javadocdir}/xerces-j2-xni \
    -Dxerces.javadoc=%{_javadocdir}/xerces-j2-impl \
    clean jar jar-xni doc #test

%install
# Jars
install -d -m 755 %{buildroot}%{_javadir}
install -p -m 644 %{name}{,-xni}-%{version}.jar %{buildroot}%{_javadir}/
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
ln -s %{name}-xni-%{version}.jar %{buildroot}%{_javadir}/%{name}-xni.jar

# Scripts
install -Dpm 755 %{SOURCE1} %{buildroot}%{_bindir}/%{name}-filter

# Samples
install -d -m 755 %{buildroot}%{_datadir}/%{name}-%{version}
install -p -m 644 %{name}-samples-%{version}.jar \
  %{buildroot}%{_datadir}/%{name}-%{version}/

# Javadocs
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a build/doc/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%doc LICENSE.txt README.txt doc/*.html
%{_bindir}/%{name}-filter
%{_javadir}/%{name}*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%doc %{_javadocdir}/*

%files demo
%{_datadir}/%{name}-%{version}

