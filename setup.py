#!/usr/bin/env python

# Copyright (c) 2018-2019 Iurii Kibalin   
# https://github.com/ikibalin/pystar  
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# 
# * Neither the name "pystar" nor the names of its contributors may
#   be used to endorse or promote products derived from this software
#   without specific prior written permission.
# 
# This software is provided by the copyright holders and contributors "as
# is" and any express or implied warranties, including, but not limited
# to, the implied warranties of merchantability and fitness for a
# particular purpose are disclaimed. In no event shall the copyright owner
# or contributors be liable for any direct, indirect, incidental, special,
# exemplary, or consequential damages (including, but not limited to,
# procurement of substitute goods or services; loss of use, data, or
# profits; or business interruption) however caused and on any theory of
# liability, whether in contract, strict liability, or tort (including
# negligence or otherwise) arising in any way out of the use of this
# software, even if advised of the possibility of such damage.


from setuptools import setup

with open("readme.md", 'r') as f:
    long_description = f.read()

setup(
    name='pystar',
    version='1.0',
    description='Reading of files with .star format',
    long_description = long_description,
    author='Iurii Kibalin',
    author_email='iurii.kibalin@cea.fr',
    url = 'https://github.com/ikibalin/pystar',
    license          = 'MIT License',
    keywords         = 'STAR',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],    
    packages=['pystar'],  #same as name
    install_requires=[
    ] #external packages as dependencies
    #scripts=[
    #        'neupy',
    #        'rhochi',
    #        'mem',
    #]
)