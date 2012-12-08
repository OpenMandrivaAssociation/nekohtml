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
Version:        1.9.6.1
Release:        %mkrel 0.0.5
Epoch:          0
Summary:        HTML scanner and tag balancer
License:        Apache License
URL:            http://nekohtml.sourceforge.net/
Source0:        http://downloads.sourceforge.net/nekohtml/nekohtml-%{version}.tar.gz
# Source 1      http://www.jpackage.org/cgi-bin/viewvc.cgi/*checkout*/rpms/devel/nekohtml/nekohtml-filter.sh?root=jpackage&content-type=text%2Fplain
Source1:        %{name}-filter.sh
Patch0:         %{name}-crosslink.patch
Patch1:         %{name}-1.9.6-jars.patch
Group:          Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  ant
BuildRequires:  java-javadoc
BuildRequires:  bcel-javadoc
BuildRequires:  xerces-j2 >= 0:2.7.1
BuildRequires:  xerces-j2-javadoc-xni
BuildRequires:  xerces-j2-javadoc-impl
Requires:       bcel
Requires:       jpackage-utils >= 0:1.6
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
%patch0 -p1
%patch1 -p1
%{_bindir}/find . -name "*.jar" | %{_bindir}/xargs -t %{__rm}
%{__perl} -pi -e 's/\r$//g' *.txt doc/*.html
%{__rm} -r doc/javadoc

%build
export CLASSPATH=$(build-classpath bcel xerces-j2)
export OPT_JAR_LIST=:
%{ant} \
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
cp -a build/doc/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

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
%doc LICENSE.txt README.txt doc/*.html
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


%changelog
* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.9.6.1-0.0.4mdv2011.0
+ Revision: 606815
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.9.6.1-0.0.3mdv2010.1
+ Revision: 523429
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.9.6.1-0.0.2mdv2010.0
+ Revision: 426249
- rebuild

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 0:1.9.6.1-0.0.1mdv2009.0
+ Revision: 168142
- fix no-buildroot-tag

* Mon Jan 28 2008 David Walluck <walluck@mandriva.org> 0:1.9.6.1-0.0.1mdv2008.1
+ Revision: 159501
- 1.9.6.1
- 1.9.6.1

* Mon Dec 17 2007 David Walluck <walluck@mandriva.org> 0:1.9.6-0.0.1mdv2008.1
+ Revision: 131550
- 1.9.6

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:0.9.5-4.1.3mdv2008.1
+ Revision: 120995
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:0.9.5-4.1.2mdv2008.0
+ Revision: 87267
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Wed Jul 04 2007 David Walluck <walluck@mandriva.org> 0:0.9.5-4.1.1mdv2008.0
+ Revision: 47860
- Import nekohtml




* Mon Feb 12 2007 Jeff Johnston <jjohnstn@redhat.com> - 0:0.9.5-4jpp.1
- Update to address Fedora review comments.

* Mon May 08 2006 Ralph Apel <r.apel at r-apel.de> - 0:0.9.5-4jpp
- First JPP-1.7 release

* Tue Oct 11 2005 Ralph Apel <r.apel at r-apel.de> - 0:0.9.5-3jpp
- Patch to JAXP13

* Mon Aug  1 2005 Ville Skyttä <scop at jpackage.org> - 0:0.9.5-2jpp
- Fix unversioned xni jar symlink (#10).

* Wed Jul  6 2005 Ville Skyttä <scop at jpackage.org> - 0:0.9.5-1jpp
- 0.9.5.

* Wed Dec 15 2004 Ville Skyttä <scop at jpackage.org> - 0:0.9.4-1jpp
- Update to 0.9.4.

* Tue Aug 24 2004 Fernando Nasser <fnasser@redhat.com> - 0:0.9.3-2jpp
- Rebuild with Ant 1.6.2

* Sat Jul  3 2004 Ville Skyttä <scop at jpackage.org> - 0:0.9.3-1jpp
- Update to 0.9.3.
- Add nekohtml-filter script.

* Thu Apr  1 2004 Ville Skyttä <scop at jpackage.org> - 0:0.9.2-1jpp
- Update to 0.9.2.

* Sat Dec 13 2003 Ville Skyttä <scop at jpackage.org> - 0:0.8.3-1jpp
- Update to 0.8.3.

* Sat Nov 15 2003 Ville Skyttä <scop at jpackage.org> - 0:0.8.2-1jpp
- Update to 0.8.2.

* Wed Oct  1 2003 Ville Skyttä <scop at jpackage.org> - 0:0.8.1-1jpp
- Update to 0.8.1.
- Crosslink with local J2SE and XNI javadocs.
- Save .spec in UTF-8.

* Thu Jun 26 2003 Ville Skyttä <scop at jpackage.org> - 0:0.7.7-1jpp
- Update to 0.7.7.

* Sun May 11 2003 David Walluck <david@anti-microsoft.org> 0:0.7.6-1jpp
- 0.7.6
- update for JPackage 1.5

* Sat Mar 29 2003 Ville Skyttä <scop at jpackage.org> - 0.7.4-2jpp
- Rebuilt for JPackage 1.5.

* Tue Mar  4 2003 Ville Skyttä <scop at jpackage.org> - 0.7.4-1jpp
- Update to 0.7.4.

* Mon Feb 24 2003 Ville Skyttä <scop at jpackage.org> - 0.7.3-1jpp
- Update to 0.7.3.
- Built with IBM's 1.3.1 SR3 and xerces-j2 2.3.0.

* Sat Jan 11 2003 Ville Skyttä <scop at jpackage.org> - 0.7.2-1jpp
- Update to 0.7.2.
- Run unit tests when building.

* Tue Dec 10 2002 Ville Skyttä <scop at jpackage.org> - 0.7.1-1jpp
- Update to 0.7.1.

* Sun Nov  3 2002 Ville Skyttä <scop at jpackage.org> - 0.6.8-1jpp
- 0.6.8, first JPackage release.
