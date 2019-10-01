## intent:apply_aggregation
- group by [application id](aggregation:application id)
- show me [total cost](target:cost) per [month](aggregation:period)
- aggregate by [app id](aggregation:application id)
- aggregate by [application id](aggregation:application id)
- show me the data on [monthly](aggregation:period) basis
- group these data by [source item](aggregation:source item)
- aggregate these data on a [source](aggregation:source) level
- apply an aggregation by [source](aggregation:source)
- aggregate the data by [source](aggregation:source)
- could you aggregate by [application id](aggregation:application id)
- I would like to see aggregation on [application id](aggregation:source) level

## intent:apply_filter
- show me data from march to october 2019
- apply filter [source](filter_name) equals [swisscom](filter_value)
- show me all [costs](target:cost) with [datarobot](filter_value) as [app id](filter_name:application id)
- give me only [costs](target:cost) for [azure](filter_value:azure) [source](filter_name)
- filter data from march to december 2018
- show me all costs for [datarobot](filter_value) [application id](filter_name)
- give me only [costs](target:cost) for [azure](filter_value) [source](filter_name)
- please, filter data from march to october 2018
- filter the data from march to october 2018
- filter from two months ago until now
- now can you further group by [application id](aggregation)
- filter from christmas 2018 until today

## intent:change_chart
- can you show me this plot as a [bubble](chart_type) plot?
- change to [bubbles](chart_type:bubble) graph
- could you show me the same graph but as [bubble's](chart_type:bubble) type?
- i would like to change the chart type to [bubble](chart_type)

## intent:clear_graph
- reset the session
- refresh a plot
- start a new graph
- can you reset the session?
- lets start from scratch
- can you clear the graph and start from scratch?
- start from scratch
- can you clean all filters and aggregations for me?

## intent:start_analysis
- show me [dsa applications](dataset:dsa applications) dataset and show me the [total cost](target:cost) of infrastructure resources.
- show me something about [dsa apps](dataset:dsa applications) [costs](target:cost)
- show me [total resource cost](target: cost) of[ dsa applications](dataset:dsa applications)
- show me some data
- show me some graphs
- could you get me information about [money spent](target:cost) on [dsa applications](dataset:dsa applications)?
- hi, can you show me some data?
- hi, show me some data
- hi, show me [total cost](target:cost) of [dsa applications](dataset:dsa applications) infrastructure
- show me cost data about [dsa apps](dataset:dsa applications)
- show me [cost](target:cost) data about [dsa apps](daltaset:dsa applications)
- show me [total cost](target:cost) of [dsa applications](dataset:dsa applications)
- give me [chatbot application](dataset:chatbot)
- show me overview of [bot app](dataset:chatbot)
- show me something about [chatbot app](dataset:chatbot)
- show me [total cost](target:cost) of [dsa applications](dataset)
- could you show me what is the [cost](target:cost) of [dsa apps](dataset:dsa applications)?
- give me data from [chatbot application](dataset:chatbot)
- show me data about [total cost](target:cost) in [dsa apps](dataset:dsa applications)
- give me some info about [chatbot](dataset:chatbot) platform
- i dont wnat to see this. can you rather show me [total cost](target:cost) of [dsa applications](dataset)?
- show me [employees](dataset:employees) data
- give me employees[employees](dataset:employees) information report
- can you show me something about [employees](dataset:employees)

## intent:start_analysis+apply_filter
- show me [cost](target:cost) data from [dsa applications](dataset:dsa applications) aggregated by [month](aggregation:period)
- give me some information about total [costs](target:cost) of [dsa apps](dataset:dsa applications) filtered from february to april 2019

## intent:remove_filter
- remove the filter
- can you please go one filter back?
- reset last filter
- delete last filtration

## intent:remove_aggregation
- remove the aggregation
- can you please go one aggregation back?
- reset last aggregation
- delete last aggregation

## synonym:cost
- total resource cost

## synonym:user
- users
- users data
- user data
- user information

## synonym:application id
- app id

## synonym:azure
- azure

## synonym:bubble
- bubbles
- bubble's

## synonym:chatbot
- chatbot application
- bot app
- chatbot app

## synonym:cost
- total cost
- costs
- money spent

## synonym:dsa applications
- dsa applications
- dsa apps
- dsa applications
- dsa apps
- dsa applications

## synonym:period
- month
- monthly

## synonym:source
- platform

