# $Id: __init__.py,v 1.11 2010/04/19 19:44:14 bruno Exp $
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
# Revision 1.11  2010/04/19 19:44:14  bruno
# added:
#
# - if "timeout == 0", then wait forever
#
# - if the user hits ctrl-c, then kill all the ssh processes associated with
#   the command. the ssh processes are killed on the local side (e.g., the
#   frontend), not the remote side
#
# Revision 1.10  2010/04/15 19:00:30  bruno
# 'rocks run host' is now 100% tentakel free!
#
# Revision 1.9  2010/02/24 22:04:25  bruno
# added a 'timeout' parameter to 'rocks run host'. idea by Tim Carlson.
#
# Revision 1.8  2009/07/13 19:34:31  bruno
# fix 'managed' flag
#
# Revision 1.7  2009/06/03 18:53:43  mjk
# - sudo support for ubuntu boy (this is cool)
# - connect to DB over the network socket not the UNIX domain socket
# - added x11 param to rocks.run.host to disable x11forwarding
#
# Revision 1.6  2009/05/27 20:15:28  bruno
# add 'managed' flag
#
# Revision 1.5  2009/05/01 19:07:02  mjk
# chimi con queso
#
# Revision 1.4  2008/10/18 00:55:57  mjk
# copyright 5.1
#
# Revision 1.3  2008/04/14 21:15:06  bruno
# let users use 'rocks run host'
#
# Revision 1.2  2008/03/06 23:41:39  mjk
# copyright storm on
#
# Revision 1.1  2008/01/29 22:13:05  bruno
# added 'rocks run host'
#
# it executes a command on all listed hosts
#
#

import threading
import os
import sys
import time
import socket
import subprocess
import shlex
import rocks.commands

class Parallel(threading.Thread):
	def __init__(self, cmdclass, cmd, host, stats, collate):
		threading.Thread.__init__(self)
		self.cmd = cmd
		self.host = host
		self.stats = stats
		self.collate = collate
		self.cmdclass = cmdclass

	def run(self):
		starttime = time.time()
		self.p = subprocess.Popen(shlex.split(self.cmd),
			stdin = subprocess.PIPE, stdout = subprocess.PIPE,
			stderr = subprocess.STDOUT)

		for line in self.p.stdout.readlines():
			if self.collate:
				self.cmdclass.addOutput(self.host, line[:-1])
			else:
				print line[:-1]

		if self.stats:
			msg = 'command on host %s took %f seconds' % \
				(self.host, time.time() - starttime)

			if self.collate:
				self.cmdclass.addOutput(self.host, msg)
			else:
				print msg

	def kill(self):
		os.kill(self.p.pid, 9)

	
class command(rocks.commands.HostArgumentProcessor,
	rocks.commands.run.command):

	MustBeRoot = 0

	
class Command(command):
	"""
	Run a command for each specified host.

	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied, the command
	is run on all known hosts.
	</arg>

	<arg type='string' name='command'>
	The command to run on the list of hosts.
	</arg>

	<arg type='boolean' name='managed'>
	Run the command only on 'managed' hosts, that is, hosts that generally
	have an ssh login. Default is 'yes'.
	</arg>

	<arg type='boolean' name='x11'>
	If 'no', disable X11 forwarding when connecting to hosts.
	Default is 'yes'.
	</arg>

	<arg type='string' name='timeout'>
	Sets the maximum length of time (in seconds) that the command is
	allowed to run.
	Default is '30'.
	</arg>

	<arg type='string' name='delay'>
	Sets the time (in seconds) to delay between each executed command
	on multiple hosts. For example, if the command is run on two
	hosts and if the delay is 10, then the command will be executed on host
	1, then 10 seconds later, the command will be executed on host 2.
	Default is '0' (no delay).
	</arg>

	<arg type='string' name='stats'>
	Display performance statistics if this parameter is set to 'yes'.
	Default is 'no'.
	</arg>

	<arg type='string' name='collate'>
	Prepend the hostname to every output line if this parameter is set to
	'yes'.
	Default is 'no'.
	</arg>

	<param type='string' name='command'>
	Can be used in place of the 'command' argument.
	</param>

	<example cmd='run host compute-0-0 command="hostname"'>
	Run the command 'hostname' on compute-0-0.
	</example>

	<example cmd='run host compute "ls /tmp"'>
	Run the command 'ls /tmp/' on all compute nodes.
	</example>
	"""

	def run(self, params, args):
		(args, command) = self.fillPositionalArgs(('command', ))

		if not command:
			self.abort('must supply a command')

		(managed, x11, t, d, stats, collate) = self.fillParams([
			('managed', 'y'),
			('x11', 'y'),
			('timeout', '30'),
			('delay', '0'),
			('stats', 'n'),
			('collate', 'n')
			])

		try:
			timeout = int(t)
		except:
			self.abort('"timeout" must be an integer')

		if timeout < 0:
			self.abort('"timeout" must be a postive integer')

		try:
			delay = float(d)
		except:
			self.abort('"delay" must be a floating point number')

		hosts = self.getHostnames(args, self.str2bool(managed))
		
		# This is the same as doing -x using ssh.  Might be useful
		# for the common case, but required for the Viz Roll.

		if not self.str2bool(x11):
			try:
				del os.environ['DISPLAY']
			except KeyError:
				pass

		if self.str2bool(collate):
			self.beginOutput()

		threads = []
		for host in hosts:
			#
			# first test if the node is up and responding to ssh
			#
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(2)
			try:
				#
				# this catches the case when the host is down
				# and/or there is no ssh daemon running
				#
				sock.connect((host, 22))

				#
				# this catches the case when the node is up,
				# sshd is sitting on port 22, but it is not
				# responding (e.g., the node is overloaded,
				# sshd is hung, etc.)
				#
				# sock.recv() should return something like:
				#
				#	SSH-2.0-OpenSSH_4.3
				#
				buf = sock.recv(64)
			except socket.error:
				if self.collate:
					self.addOutput(host, 'down')
				else:
					print '%s: down'		

				continue

			cmd = 'ssh %s "%s"' % (host, sys.argv[-1])

			p = Parallel(self, cmd, host, self.str2bool(stats),
				self.str2bool(collate))
			p.start()
			threads.append(p)

			if delay > 0:
				time.sleep(delay)

		#
		# collect the threads
		#
		try:
			totaltime = time.time()
			while timeout == 0 or \
					(time.time() - totaltime) < timeout:

				active = threading.enumerate()

				if len(active) == 1:
					break
				
				t = threads
				for thread in t:
					if thread not in active:
						thread.join(0.1)
						threads.remove(thread)

				#
				# don't burn a CPU while waiting for the
				# threads to complete
				#
				time.sleep(0.5)

		except KeyboardInterrupt:
			#
			# try to collect all the active threads
			#
			active = threading.enumerate()

			t = threads
			for thread in t:
				if thread not in active:
					thread.join(0.1)
					threads.remove(thread)

		#
		# kill all still active threads
		#
		active = threading.enumerate()
		if len(active) >= 2:
			for i in range(1, len(active)):
				active[i].kill()

		if self.str2bool(collate):
			self.endOutput(padChar='')
