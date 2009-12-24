##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import sys
from cStringIO import StringIO
from profiler import getStats, installProfiler, uninstallProfiler


class Profiler(object):

    def listStats(self):
        stats = []
        for uri, info in getStats().items():
            stats.append({'uri': uri, 'calls': info[2]})

        return stats

    def viewStats(self):
        stats = getStats()
        request = self.request

        if not stats:
            return ''

        uri = request.get('stats', None)

        info = stats.get(uri)
        if not info:
            info = stats.items()[0][1]

        stats = info[0]

        output = StringIO()

        stripdirs = request.get('stripdirs', False)
        if stripdirs:
            stats.strip_dirs()

        sorton = request.get('sorton', 'time')
        stats.sort_stats(sorton)

        mode = request.get('mode', 'stats')
        stdnameRe = request.get('stdnameRe', '')
        limit = int(request.get('limit', 500))

        if stdnameRe:
            stats.setOutputFile(output)
            getattr(stats, 'show%s' % mode.capitalize())(str(stdnameRe), limit)
            res = output.getvalue()
            if not res: 
                res = 'No matching functions'
            return res
        else:
            stats.stream = output

            try:
                getattr(stats, 'print_%s'%mode)(limit)
            finally:
                pass

            return output.getvalue()

    def __call__(self):
        request = self.request

        if 'profile.install' in request:
            calls = int(request.get('calls', 2))
            installProfiler(calls)

        return self.index()
