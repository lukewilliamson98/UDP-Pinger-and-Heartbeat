# Use iperf as traffic generator
import sys
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel


link100MNoLoss = dict(bw = 100, delay='5ms', loss=0, max_queue_size=1000, use_htb=True)
links1s2 = dict(bw = 50, delay='5ms', loss=0, max_queue_size=500, use_htb=True)

class DualSwitchTopo(Topo):
	"Dual switch connected to n hosts"
	def build(self):
		switch1 = self.addSwitch('s1')
		host1 = self.addHost('h1')
		self.addLink(host1, switch1, **link100MNoLoss)

		host3 = self.addHost('h3')
		self.addLink(host3, switch1, **link100MNoLoss)

		switch2 = self.addSwitch('s2')
		host2= self.addHost('h2')
		self.addLink(host2, switch2, **link100MNoLoss)

		host4 = self.addHost('h4')
		self.addLink(host4, switch2, **link100MNoLoss)

		host5 = self.addHost('h5')
		self.addLink(host5, switch1, **link100MNoLoss)

		host6 = self.addHost('h6')
		self.addLink(host6, switch2, **link100MNoLoss)
		self.addLink(switch1, switch2, **links1s2)

def perfTest():
	"Create network and run simple perf test"
	topo = DualSwitchTopo()
	net = Mininet(topo=topo,
			 link=TCLink)
	net.start()
	print "Dumping host connections"
	dumpNodeConnections(net.hosts)
	print "Testing network connectivity"
	net.pingAll()
	c0, h1, h2, h3, h4, h5, h6 = net.get('c0','h1', 'h2', 'h3', 'h4', 'h5', 'h6')
	print "IP address of h6 is ", h6.IP()
	CLI(net)
	net.stop()

if __name__ == '__main__':
	# tell mininet to print useful info
	setLogLevel('info')
	perfTest()

