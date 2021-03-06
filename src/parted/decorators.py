#
# Python bindings for libparted (built on top of the _ped Python module).
#
# Copyright (C) 2009 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Peter Jones <pjones@redhat.com>
#

import locale
import functools

def localeC(fn):
    # setlocale is not thread-safe, and anaconda (at least) may call this from
    # another thread.  This is just a luxury to have untranslated tracebacks,
    # so it's not worth tracebacking itself.
    def _setlocale(l):
        try:
            locale.setlocale(locale.LC_MESSAGES, l)
        except:
            pass

    @functools.wraps(fn)
    def new(*args, **kwds):
        oldlocale = locale.getlocale(locale.LC_MESSAGES)
        _setlocale('C')
        try:
            ret = fn(*args, **kwds)
        finally:
            _setlocale(oldlocale)
        return ret
    return new
