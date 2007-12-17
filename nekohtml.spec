# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define section free
%define gcj_support 1

Name:           nekohtml
Version:        0.9.5
Release:        %mkrel 4.1.3
Epoch:          0
Summary:        HTML scanner and tag balancer
License:        Apache License
URL:            http://www.apache.org/~andyc/neko/doc/html/
Source0:        http://www.apache.org/~andyc/neko/nekohtml-0.9.5.tar.gz
# Source 1      http://www.jpackage.org/cgi-bin/viewvc.cgi/*checkout*/rpms/devel/nekohtml/nekohtml-filter.sh?root=jpackage&content-type=text%2Fplain
Source1:        %{name}-filter.sh
Patch0:         %{name}-crosslink.patch
Patch1:         %{name}-HTMLScanner.patch
Group:          Development/Java

%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  ant
BuildRequires:  java-javadoc
BuildRequires:  xerces-j2 >= 0:2.7.1
BuildRequires:  xerces-j2-javadoc-xni
BuildRequires:  xerces-j2-javadoc-impl
Requires:               jpackage-utils >= 0:1.6
Requires:       xerces-j2 >= 0:2.7.1

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
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:               jpackage-utils >= 0:1.6
Requires(postun):       jpackage-utils >= 0:1.6

%description    javadoc
Javadoc for %{name}.

%package        demo
Summary:        Demo for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:               jpackage-utils >= 0:1.6
Requires(postun):       jpackage-utils >= 0:1.6

%description    demo
Demonstrations and samples for %{name}.


%prep
%setup -q
%patch0 -p0
%patch1 -b .sav
find . -name "*.jar" -exec rm -f {} \;


%build
export CLASSPATH=$(build-classpath xerces-j2)
%{ant} -f build-html.xml \
    -Djarfile=%{name}-%{version}.jar \
    -DjarfileXni=%{name}-xni-%{version}.jar \
    -DjarfileSamples=%{name}-samples-%{version}.jar \
    -Dj2se.javadoc=%{_javadocdir}/java \
    -Dxni.javadoc=%{_javadocdir}/xerces-j2-xni \
    -Dxerces.javadoc=%{_javadocdir}/xerces-j2-impl \
    clean package jar-xni test


%install
rm -rf $RPM_BUILD_ROOT

# Jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 644 %{name}{,-xni}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -s %{name}-xni-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-xni.jar

# Scripts
install -Dpm 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/%{name}-filter

# Samples
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
install -p -m 644 %{name}-samples-%{version}.jar \
  $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/

# Javadocs
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr bin/package/nekohtml-*/doc/html/javadoc/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/

# Avoid having javadocs in %doc.
rm -rf bin/package/nekohtml-*/doc/html/javadoc

# Fix EOL in files
pushd bin/package/nekohtml-*/doc/html
for x in *.html; do tr -d \\r <$x >$x.tmp; mv $x.tmp $x; done
tr -d \\r <.htaccess >.htaccess.tmp; mv .htaccess.tmp .htaccess
# Rename .htaccess file to sample version.
mv .htaccess sample.htaccess
# ln -sf %{_javadocdir}/%{name}-%{version} javadoc
popd

pushd bin/package/nekohtml-*/doc
tr -d \\r <style.css >style.css.tmp; mv style.css.tmp style.css
popd 

for x in LICENSE*; do tr -d \\r <$x >$x.tmp; mv $x.tmp $x; done
for x in README*; do tr -d \\r <$x >$x.tmp; mv $x.tmp $x; done
for x in TODO*; do tr -d \\r <$x >$x.tmp; mv $x.tmp $x; done

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE* README* TODO* bin/package/nekohtml-*/doc/*
%attr(755,root,root) %{_bindir}/%{name}-filter
%{_javadir}/%{name}*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/*

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}-%{version}
