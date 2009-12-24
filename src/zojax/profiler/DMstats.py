# Copyright (C) 2006 by Dr. Dieter Maurer, Eichendorffstr. 23, D-66386 St. Ingbert, Germany
# see "LICENSE.txt" for details
#       $Id$
''''Stats' enhancements.

The module defines 'Stats' which inherits from Pythons 'Stats'
and enhances it by methods 'showCallees(funRe)', 'showCallers(funRe)'
and 'showStats(funRe)' which extracts information for functions
matched by the regular expression *funRe*.
This can make profile analysis significantly easier.
'''

from pstats import Stats as pStats
from sys import stdout
from re import compile
from StringIO import StringIO


class Stats(pStats):

  def setOutputFile(self, file):
    self._out = file

  def showCallees(self, *amount):
    msg, fs = self._selectFunctions(amount)
    self._print(msg)
    for f in fs: self._showCallees(f); self._print('\n')

  def showStats(self, *amount):
    msg, fs = self._selectFunctions(amount)
    self._print(msg)
    for f in fs: self._showStats(f)

  def showCallers(self, *amount):
    msg, fs = self._selectFunctions(amount)
    self._print(msg)
    for f in fs: self._showCallers(f); self._print('\n')

  def _selectFunctions(self, amount):
    if self.fcn_list:
      l = self.fcn_list
      msg = "   Ordered by: " + self.sort_type + '\n'
    else:
      l = self.stats.keys()
      msg = "   Unordered\n"
    for sel in amount:
      l, msg = self.eval_print_amount(sel, l, msg)
    return msg, l

  def _showCallees(self, f):
    self._showStats(f)
    self.calc_callees()
    callees = self.all_callees.get(f)
    if not callees: return
    stats = self.stats; format = self._formatFunction
    for (cf, calls) in callees.iteritems():
      scf = stats[cf]
      try:
        self._print('\t%4dc\t(of %4dc in %8.3fs)\t%s\n'
                    % (calls, scf[1], scf[3], format(cf), ))
      except:
        self._print('\t%4dc\t(of %4dc in %8.3fs)\t%s\n'
                    % (calls[0], scf[1], scf[3], format(cf), ))

  def _showCallers(self, f):
    self._showStats(f)
    stats = self.stats; format = self._formatFunction
    mstat = stats[f]
    for (cf, calls) in mstat[4].iteritems():
      scf = stats[cf]
      try:
        self._print('\t%4dc\t(from %4dc in %8.3fs)\t%s\n'
                    % (calls, scf[1], scf[3], format(cf), )
                    )
      except:
        self._print('\t%4dc\t(from %4dc in %8.3fs)\t%s\n'
                    % (calls[0], scf[1], scf[3], format(cf), )
                    )

  def _formatFunction(self, ft):
    return '%s:%s(%s)' % ft

  def _showStats(self, ft):
    s = self.stats[ft]
    self._print('%4dc - %8.3fs %8.3fs/c - %8.3fs %8.3fs/c - %s\n' % (
      s[1], s[2], s[2]/s[1], s[3], s[3]/s[1], self._formatFunction(ft),
      )
                )

  def _print(self, txt):
    self._out.write(txt)
