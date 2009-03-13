# $Id: __init__.py,v 1.1 2009/03/13 00:03:00 mjk Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
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
# Revision 1.1  2009/03/13 00:03:00  mjk
# - checkpoint for route commands
# - gateway is dead (now a default route)
# - removed comment rows from schema (let's see what breaks)
# - removed short-name from appliance (let's see what breaks)
# - dbreport static-routes is dead
#

import sys
import socket
import rocks.commands
import string

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.report.command):

	def getRoute(self, network, netmask, gateway):

		s = 'any '

		# Skip the default route (reported elsewhere)
		
		if network == '0.0.0.0' and netmask == '0.0.0.0':
			return None
			
		# Is the a host or network route?
				
		if netmask == '255.255.255.255':
			s += 'host %s ' % network
		else:
			s += 'net %s netmask %s ' % (network, netmask)
			
		# Is this a gateway or device route?
				
		if gateway.count('.') == 3:
			s += 'gw %s' % gateway
		else:
			s += 'dev %s' % gateway
			
		return s
		
	
	def run(self, params, args):

		self.beginOutput()

		for host in self.getHostnames(args):
			routes = self.db.getHostRoutes(host)
			for (key, val) in routes.items():
				s = self.getRoute(key, val[0], val[1])
				if s:
					self.addOutput(host, s)

		self.endOutput(padChar='')

