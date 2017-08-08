"""
To use named tupple : Tuple
"""

from collections import namedtuple

support = namedtuple('SDSupport','CQ,Cache,maint')
ins1 = support('Enable','Disable','supported')
print 'cache %s'%ins1.Cache
#cache Disable
print 'CQ %s'%ins1.CQ
#CQ Enable
print 'maint %s'%ins1.maint