# Case Study: markets-unlimited.com

In the data, I found that there were several accesses from a site called markets-unlimited.com, but not much traffic.
We found this interesting and decided to look into it more, since there was no website at the address. We were suspicious that this site could be malware.

## Timeline of accesses to and from markets-unlimited.com

<object width="100%" height="400" type="text/html" data="graphs/markets-unlimited/domain_accesses_timeline_chart.html"></object>

Most of the time, the accesses are pretty consistent, at less than 1000 accesses per hour. However, there's a period of time between noon on May 12th and noon on May 14th where the accesses spike, and this is also the same time period where a lot of the traffic in the network
from other sites decreases greatly.

## Gantt Chart of the timeline of accesses to markets-unlimited.com

<object width="100%" height="100" type="text/html" data="graphs/markets-unlimited/domain_gantt_timeline_chart.html"></object>

The site is accessed regularly, while the network is up, since the chunks of accesses are solid between 4AM and 11PM.

## Traffic to each port from markets-unlimited.com

<object width="100%" height="400" type="text/html" data="graphs/markets-unlimited/domain_ports_traffic_chart.html"></object>

Most of the traffic has a public port 53, which is DNS. Since malware sites sometimes use port 53 to disguise their traffic as DNS, 
we can be suspicious of this address.

## Size of traffic per flow to and from markets-unlimited.com

<object width="100%" height="400" type="text/html" data="graphs/markets-unlimited/domain_traffic_flows_chart.html"></object>

Most flows transport around 40-55 bytes of data per flow. (This graph was made mainly to check if the site had consistently the same amount of traffic per flow - like periodical accesses.)

## Timeline of traffic to and from markets-unlimited.com

<object width="100%" height="400" type="text/html" data="graphs/markets-unlimited/domain_traffic_timeline_chart.html"></object>

Similar to the accesses, most of the time the traffic is pretty consistent, at less than 1000 accesses per hour. However, there's a period of time between noon on May 12th and noon on May 14th where the traffic spikes, and this is also the same time period where a lot of the traffic in the network from other sites decreases greatly.

## Total traffic per user to and from markets-unlimited.com

<object width="100%" height="400" type="text/html" data="graphs/markets-unlimited/domain_users_traffic_chart.html"></object>

This graph was originally made to see if the potential malware was affecting only a few of the users, rather than many of them. However,
we saw that most, if not all, users had traffic running to and from this site, so this evidence would support an argument against whether or not markets-unlimited.com is malware.
