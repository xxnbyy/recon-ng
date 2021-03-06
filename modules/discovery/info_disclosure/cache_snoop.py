import module
# module specific packages
import os
import dns
import re

class Module(module.Module):

    def __init__(self, params):
        module.Module.__init__(self, params)
        # could look up the nameserver for each domain and loop
        self.register_option('nameserver', self._global_options['nameserver'], True, 'ip address of target\'s nameserver')
        self.register_option('domains', self.data_path+'/av_domains.lst', True, 'file containing the list of domains to snoop for')
        self.info = {
            'Name': 'DNS Cache Snooper',
            'Author': 'thrapt (thrapt@gmail.com)',
            'Description': 'Uses the DNS cache snooping technique to check for visited domains',
            'Comments': [
                'Nameserver must be in IP form.',
                'http://304geeks.blogspot.com/2013/01/dns-scraping-for-corporate-av-detection.html'
            ]
        }

    def module_run(self):
        nameserver = self.options['nameserver']
        with open(self.options['domains']) as fp:
            domains = [x.strip() for x in fp.read().split()]
        for domain in domains:
            response = None
            # prepare our query
            query = dns.message.make_query(domain, dns.rdatatype.A, dns.rdataclass.IN)
            # unset the Recurse flag 
            query.flags ^= dns.flags.RD
            response = dns.query.udp(query, nameserver)
            if len(response.answer) > 0:
                self.alert('%s => Snooped!' % (domain))
            else:
                self.verbose('%s => Not Found.' % (domain))
