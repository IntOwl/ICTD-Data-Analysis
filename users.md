# Data distributed over Users

## Timeline of Traffic per User (Daily)

<object width="100%" height="400" type="text/html" data="graphs/users/user_distr_daily_timeline_chart.html"></object>

Select a user from the dropdown menu to see how much traffic they use per day.

## Traffic from Users per Day as a Distribution over All Users:

### Violin Plot

<object width="100%" height="400" type="text/html" data="graphs/users/daily_traffic_user_distr_violin.html"></object>

The amount of traffic used by each user per day, plotted over all users and all days in the dataset. The thicker the line, the more users have used an amount of traffic close to the number given (exact numbers would take up too much space, so many of the numbers here are binned into categories to plot over).

### Box Plot

<object width="100%" height="400" type="text/html" data="graphs/users/daily_traffic_user_distr_boxplot.html"></object>

The amount of traffic used by each user per day, plotted over all users and all days in the dataset. Each day has its own boxplot with each datapoint in the boxplot being a user that has used a specific amount of data. 

### Ridgeline Plot

<object width="100%" height="400" type="text/html" data="graphs/users/user_traffic_daily_distr_ridgeline.html"></object>

Similar to the violin plot but slightly easier to visualize (and looking less like Christmas ornaments), this ridgeline plot takes the data of each user's total traffic per day and bins it, then graphs all the bins over each day. The bigger bumps in each day's plot represent more users with total daily traffic in that area.

## Traffic by Users as Distribution over All Users:

### Violin Plot (Hourly)

<object width="100%" height="400" type="text/html" data="graphs/users/user_distr_traffic_hourly_violin.html"></object>

The amount of traffic used by each user, per hour, categorized into a plot of how often they use each amount of traffic and separated out by user. The thicker the line, the more often the user has used that amount of traffic in a day, and vice versa.

### Violin Plot (Daily)

<object width="100%" height="400" type="text/html" data="graphs/users/user_distr_traffic_daily_violin.html"></object>

The amount of traffic used by each user, per day, categorized into a plot of how often they use each amount of traffic and separated out by user. The thicker the line, the more often the user has used that amount of traffic in a day, and vice versa.

### Boxplot (Hourly)

<object width="100%" height="400" type="text/html" data="graphs/users/user_distr_traffic_hourly_boxplot.html"></object>

A distribution of traffic used by each user, per hour. The boxes represent the 25th to the 75th percentile of traffic for that user, and the lines below and above represent the 0-25th and 75th-100th percentiles, respectively.

### Boxplot (Daily)

<object width="100%" height="400" type="text/html" data="graphs/users/user_distr_traffic_daily_boxplot.html"></object>

A distribution of traffic used by each user, per day. The boxes represent the 25th to the 75th percentile of traffic for that user, and the lines below and above represent the 0-25th and 75th-100th percentiles, respectively.
