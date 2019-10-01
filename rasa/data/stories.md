## path 1
* start_analysis {"dataset":"dsainfo", "target":"cost"}
 - action_start_analysis
* apply_filter {"filter_value":"azure", "filter_name":"source"}
 - action_apply_filter
* apply_aggregation {"aggregation":"period"}
 - action_apply_aggregation

## path 2

* start_analysis{"target":"cost","dataset":"dsainfo"}
 - action_start_analysis
* apply_aggregation{"aggregation":"source"}
 - action_apply_aggregation
* apply_filter{"time": {"to": "2018-12-01T00:00:00.000-07:00", "from": "2018-03-01T00:00:00.000-08:00"}}
 - action_apply_filter
* clear_graph
 - action_clear_graph

## interactive_story_2
* start_analysis{"target": "cost", "dataset": "dsa applications"}
    - action_start_analysis
* apply_aggregation{"aggregation": "source"}
    - action_apply_aggregation
* apply_filter {"time": {"to": "2018-12-01T00:00:00.000-07:00", "from": "2018-03-01T00:00:00.000-08:00"}}
    - action_apply_filter

## interactive_story_2
* start_analysis{"target": "cost", "dataset": "dsa applications"}
    - action_start_analysis
* apply_aggregation{"aggregation": "source"}
    - action_apply_aggregation
* apply_aggregation{"aggregation": "application id"}
    - action_apply_aggregation
* apply_filter {"time": {"to": "2018-12-01T00:00:00.000-07:00", "from": "2018-03-01T00:00:00.000-08:00"}}
    - action_apply_filter


## change story in the middle
* start_analysis{"target": "cost", "dataset": "dsa applications"}
    - action_start_analysis
* start_analysis{"target": "user", "dataset": "chatbot"}
    - action_start_analysis


## main_story
* start_analysis{"dataset": "dsa applications","target":"cost"}
    - action_start_analysis
* remove_aggregation
    - action_remove_aggregation
* apply_aggregation{"aggregation":"source"}
    - action_apply_aggregation
* apply_aggregation{"aggregation":"application id"}
    - action_apply_aggregation
* apply_filter{"time": {"to": "2018-11-01T00:00:00.000-07:00", "from": "2018-03-01T00:00:00.000-08:00"}}
    - action_apply_filter
* remove_filter
    - action_remove_filter
* apply_filter{"time": {"to": "2018-12-01T00:00:00.000-07:00", "from": "2018-03-01T00:00:00.000-08:00"}}
    - action_apply_filter



## interactive_story_1
* start_analysis{"target": "cost", "dataset": "dsa applications"}
    - action_start_analysis
* apply_aggregation{"aggregation": "source"}
    - action_apply_aggregation
* apply_filter{"time": {"to": "2018-11-01T00:00:00.000-07:00", "from": "2018-03-01T00:00:00.000-08:00"}}
    - action_apply_filter
* clear_graph
    - action_clear_graph

## interactive_story_2
* start_analysis{"target": "cost", "dataset": "dsa applications"}
    - action_start_analysis
* apply_aggregation{"aggregation": "source"}
    - action_apply_aggregation
* apply_aggregation{"aggregation": "application id", "time": "2019-09-25T17:10:54.000-07:00"}
    - action_apply_aggregation
* change_chart{"chart_type": "bubble"}
    - action_change_chart

## interactive_story_3
* start_analysis{"target": "user", "dataset": "chatbot"}
    - action_start_analysis
* start_analysis{"target": "cost", "dataset": "dsa applications"}
    - action_start_analysis
* apply_filter{"time": {"to": "2019-09-26T00:00:00.000-07:00", "from": "2018-12-25T00:00:00.000-08:00"}}
    - action_apply_filter
* start_analysis{"target": "user", "dataset": "chatbot", "time": "2019-09-25T17:22:22.000-07:00"}
    - action_start_analysis

## two intents together
* start_analysis+apply_filter{"target": "cost", "dataset": "dsa applications", "time":{"from":"2018-12-25T00:00:00.000-08:00", "to":"2019-09-25T17:22:22.000-07:00"}}
    - action_apply_filter

## no data case
* start_analysis
   - action_start_analysis
* start_analysis{"dataset":"dsa applications"}
   - action_start_analysis
* start_analysis{"target":"cost"}
   - action_start_analysis

## story 5
* start_analysis{"target": "cost", "dataset": "dsa applications"}
   - action_start_analysis
* remove_aggregation
   - action_remove_aggregation
* apply_aggregation {"aggregation":"application id"}
   - action_apply_aggregation
* apply_aggregation {"aggregation":"source"}
   - action_apply_aggregation
* remove_aggregation
   - action_remove_aggregation
* apply_filter{"time":{"from":"2018-12-25T00:00:00.000-08:00", "to":"2019-09-25T17:22:22.000-07:00"}}
   - action_apply_filter
* remove_filter
   - action_remove_filter
* start_analysis{"dataset": "chatbot"}
   - action_start_analysis
