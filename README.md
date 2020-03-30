# ZZ-compute

### Description
Service is ment to execute model inference. Optionally it can execute third-party 
Python code (mostly provided by data scientists).

### Security
 - Third party Python code will be executed via [CodelJail](https://github.com/edx/codejail)
 - The code will be tested on FAS-node by [Pyt](https://github.com/python-security/pyt)
 - [Apparmour in OpenShift](https://docs.openshift.com/container-platform/3.10/admin_guide/disabling_features.html)
 
 ##### Dockerfile
 ```Dockerfile

RUN wget -qO- https://bitbucket.org/pypy/pypy/downloads/pypy3.6-v7.3.0-src.tar.bz2 | tar -xvjf - && \
    mv pypy3* pypy3

RUN cd pypy3/pypy/goal && \
    sed -i '/print __doc__/d' ../../rpython/bin/rpython && \
    sed -i '/Default target: /d' ../../rpython/translator/goal/translate.py && \
    sed -i '/print "Run/d' ../../rpython/translator/goal/translate.py && \
    sed -i '/translateconfig.targetspec)/d' ../../rpython/translator/goal/translate.py && \
    sed -i '/\n\nTarget specific/d' ../../rpython/translator/goal/translate.py && \
    sed -i '/translateconfig.targetspec,)/d' ../../rpython/translator/goal/translate.py && \
    sed -i '/No target-specific help/d' ../../rpython/translator/goal/translate.py && \
    sed -i '/Target specific help/d' ../../rpython/translator/goal/translate.py && \
    sed -i '/For detailed descriptions/d' ../../rpython/translator/goal/translate.py && \
    sed -i 's/pypy.readthedocs.org/pass/g' ../../rpython/translator/goal/translate.py && \
    pypy3 ../../rpython/bin/rpython -O2 --sandbox targetpypystandalone
``` 