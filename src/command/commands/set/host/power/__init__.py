# $Id: __init__.py,v 1.3 2010/06/25 19:10:07 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: __init__.py,v $
# Revision 1.3  2010/06/25 19:10:07  bruno
# let non-root users control the power to nodes
#
# Revision 1.2  2010/06/23 22:51:11  bruno
# fix
#
# Revision 1.1  2010/06/22 21:42:36  bruno
# power control and console access for VMs
#
#

import rocks.commands
import os

class command(rocks.commands.set.host.command):
	MustBeRoot = 0


class Command(command):
	"""
	Set the power for a host. Power settings can be 'on' or 'off.

	<arg type='string' name='host' repeat='1'>
	One or more host names.
	</arg>

	<param type='string' name='switch'>
	The power setting. This must be one of 'on' or 'off.
	</param>

	<param type='string' name='key' optional='1'>
	A private key that will be used to authenticate the request. This
        should be a file name that contains the private key.
	</param>
		
	<example cmd='set host power compute-0-0 switch=on'>
	Turn on the power for compute-0-0.
	</example>
	"""

	def run(self, params, args):
		(switch, key) = self.fillParams([
			('switch', ),
			('key', )
			])
		
		if not len(args):
			self.abort('must supply at least one host')

		if switch not in [ 'on', 'off' ]:
			self.abort('invalid switch value. ' +
				'switch must be "on" or "off"')

		if key and not os.path.exists(key):
			self.abort("can't access the private key '%s'" % key)

		for host in self.getHostnames(args):
			#
			# run the plugins
			# 
			self.runPlugins([host, switch, key])

