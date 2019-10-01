# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/
#
#
# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
import json
import datetime

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


def create_dict(data_type, dataset, target, filter_list=None, aggregation_list=None, chart_type=None):
    dict_ = dict({"data_type": data_type, "dataset": dataset, "target": target, "aggregation_list": aggregation_list,
                "filter_list": filter_list, "chart_type": chart_type})
    return dict_

def required_data_available(slots):
    missing_variables = []
    if slots["dataset"] is None:
        missing_variables.append("dataset")
        if slots["target"] is None:
            missing_variables.append("target")
    else:
        if DataStorage.dataset_properties[slots["dataset"]]["data_type"]!="report":
            if slots["target"] is None:
                missing_variables.append("target variable")
        else:
            slots["target"] = "dummy_target"

    message = "I am missing some information in order to create a graph. Could you tell me more about following variables {}?".format(missing_variables)

    if len(missing_variables)==0:
        return True, "", slots

    return False, message, slots

def merge_old_and_new(old,new):
    if old is not None:
        old = json.loads(old)
        old.append(new)
        new = old
    else:
        new = [new]
    return json.dumps(new) 


class DataStorage():

    datasets = ["dsa applications"]
    reports = ["chatbot","employees"]

    graph_data_keys = ["data_type","dataset","target","aggregation","filter","chart_type"]

    dataset_properties = {
        "dsa applications": {
            "data_type": "dataset",
            "basicPlot": create_dict(data_type="dataset", dataset="dsa applications", target="cost",aggregation_list=["period"], filter_list=None, chart_type="bar"),
            "message": "I am showing you a default plot for chosen target variable. If you want to see more, you can apply filters and aggregations in following dimensions: Source, Application ID, Period, Source Item",
            "dimensions": ["Source", "Application ID","Period","Source Item"]       
        },
        "chatbot": {
            "data_type": "report",
            "basicPlot": create_dict(data_type="report", dataset="chatbot", target="dummy target"),
            "message": "This is an interactive report. You can investigate it by clicking around, but there is no voice control. Enjoy!"
        },
        "employees": {
            "data_type": "report",
            "basicPlot": create_dict(data_type="report", dataset="employees", target="dummy target"),
            "message": "This is an interactive report. You can investigate it by clicking around, but there is no voice control. Enjoy!"
        }
    }


class ActionStartAnalysis(Action):

    def name(self) -> Text:
        return "action_start_analysis"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        events = []

        entities = {entity["entity"]: entity["value"] for entity in tracker.latest_message['entities']}
        slots = tracker.current_slot_values()

        if "dataset" in entities.keys() or "target" in entities.keys():
            slots = {key:None for key,value in slots.items()}
            for name,value in entities.items():
                slots[name] = value

        is_available, message, slots = required_data_available(slots)


        if is_available:
            dataset = slots["dataset"]

            graph_data = DataStorage.dataset_properties[dataset]["basicPlot"]
            message = DataStorage.dataset_properties[dataset]["message"]

            dispatcher.utter_message(json.dumps({"graph_data":graph_data, "message": message}))
            events = [SlotSet(slot_name,slot_value) for slot_name, slot_value in graph_data.items()]
        else:
            dispatcher.utter_message(json.dumps({"graph_data": None, "message":message}))
        return events

        


class ActionApplyFilter(Action):

    def name(self) -> Text:
        return "action_apply_filter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        events = []

        entities = {entity["entity"]: entity["value"] for entity in tracker.latest_message['entities']}
        slots = tracker.current_slot_values()

        is_available, message, slots = required_data_available(slots)

        if is_available:

            data_type = DataStorage.dataset_properties[slots["dataset"]]["data_type"]

            if data_type=="dataset":

                if "time" in entities.keys():
                    time = entities["time"]
                    filter_name = "period"
                    filter_value = self.create_time_filter_string(time["from"], time["to"])
                elif "filter_name" in entities.keys() and "filter_value" in entities.keys():
                    filter_name = entities["filter_name"]
                    filter_value = entities["filter_value"]
                else:
                    # TODO
                    return

                filter_new = {"filter_name":filter_name, "filter_value": filter_value}
                filter_old = slots["filter_list"]
                if filter_old is not None:
                    filter_new = filter_old + [filter_new]
                else:
                    filter_new = [filter_new]

                graph_data = slots
                graph_data["filter_list"] = filter_new
                graph_data["data_type"] = data_type
                dispatcher.utter_message(json.dumps({"graph_data":graph_data, "message": None}))

                events = [SlotSet("filter_list", filter_new), SlotSet("data_type", data_type)]
            else:
                message = "This operation can not be applied to this data."
                dispatcher.utter_message(json.dumps({"graph_data": None, "message":message}))
        else:
            dispatcher.utter_message(json.dumps({"graph_data": None, "message":message}))
        return events

    @staticmethod
    def create_time_filter_string(time_from, time_to):
        time_from = datetime.datetime.strptime(time_from[:23],"%Y-%m-%dT%H:%M:%S.%f")
        time_to = datetime.datetime.strptime(time_to[:23],"%Y-%m-%dT%H:%M:%S.%f")
        return "{}-{}_{}-{}".format(time_from.year,time_from.month,time_to.year,time_to.month)



class ActionRemoveFilter(Action):

    def name(self) -> Text:
        return "action_remove_filter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        events = []

        slots = tracker.current_slot_values()

        is_available, message, slots = required_data_available(slots)

        if is_available:

            data_type = DataStorage.dataset_properties[slots["dataset"]]["data_type"]

            if data_type=="dataset":

                if slots["filter_list"] is not None:

                    filter_list = slots["filter_list"]

                    if len(filter_list)>1:
                        print(filter_list)
                        filter_list = filter_list[:-1]
                    else:
                        filter_list = None

                    graph_data = slots
                    graph_data["filter_list"] = filter_list
                    graph_data["data_type"] = data_type
                    dispatcher.utter_message(json.dumps({"graph_data": graph_data, "message":None}))
                    events = [SlotSet("filter_list",filter_list),SlotSet("data_type",data_type)]
                else:
                    message = "There are no filters to remove."
                    dispatcher.utter_message(json.dumps({"graph_data": None, "message":message}))
            else:
                message = "This operation can not be applied to this data."
                dispatcher.utter_message(json.dumps({"graph_data": None, "message":message}))
        else:
            dispatcher.utter_message(json.dumps({"graph_data": None, "message":message}))
        return events


class ActionApplyAggregation(Action):

    def name(self) -> Text:
        return "action_apply_aggregation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        events = []

        entities = {entity["entity"]: entity["value"] for entity in tracker.latest_message['entities']}
        slots = tracker.current_slot_values()

        is_available, message, slots = required_data_available(slots)

        if is_available:

            data_type = DataStorage.dataset_properties[slots["dataset"]]["data_type"]

            if data_type=="dataset":

                if "aggregation" in entities.keys():
                    aggregation_new = entities["aggregation"]
                    aggregation_old = slots["aggregation_list"]
                    if aggregation_old is not None:
                        aggregation_new = aggregation_old + [aggregation_new]
                    else:
                        aggregation_new = [aggregation_new]
                else:
                    # TODO
                    return

                graph_data = slots
                graph_data["aggregation_list"] = aggregation_new
                graph_data["data_type"] = data_type
                dispatcher.utter_message(json.dumps({"graph_data":graph_data, "message": message}))

                events = [SlotSet("aggregation_list",aggregation_new), SlotSet("data_type", data_type)]
            else:
                message = "This operation can not be applied to this data."
                dispatcher.utter_message(json.dumps({"graph_data": None, "message":message}))
        else:
            dispatcher.utter_message(json.dumps({"graph_data": None, "message":message}))
        return events


class ActionRemoveAggregation(Action):

    def name(self) -> Text:
        return "action_remove_aggregation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        events = []

        slots = tracker.current_slot_values()

        is_available, message, slots = required_data_available(slots)

        if is_available:

            data_type = DataStorage.dataset_properties[slots["dataset"]]["data_type"]

            if data_type=="dataset":

                if slots["aggregation_list"] is not None:

                    aggregation_list = slots["aggregation_list"]

                    if len(aggregation_list)>1:
                        aggregation_list = aggregation_list[:-1]
                    else:
                        aggregation_list = None

                    graph_data = slots
                    graph_data["aggregation_list"] = aggregation_list
                    graph_data["data_type"] = data_type
                    dispatcher.utter_message(json.dumps({"graph_data": graph_data, "message":None}))
                    events = [SlotSet("aggregation_list",aggregation_list), SlotSet("data_type",data_type)]
                else:
                    message = "There are no filters to remove."
                    dispatcher.utter_message(json.dumps({"graph_data": None, "message":message}))
            else:
                message = "This operation can not be applied to this data."
                dispatcher.utter_message(json.dumps({"graph_data": None, "message":message}))
        else:
            dispatcher.utter_message(json.dumps({"graph_data": None, "message":message}))
        return events


class ActionClearGraph(Action):

    def name(self) -> Text:
        return "action_clear_graph"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        events = []

        slots = tracker.current_slot_values()

        is_available, message, slots = required_data_available(slots)

        if is_available:

            graph_data = DataStorage.dataset_properties[slots["dataset"]]["basicPlot"]

            message = "I have cleared the graph and I am showing you a default plot for this dataset."

            dispatcher.utter_message(json.dumps({"graph_data":graph_data, "message": message}))

            events = [SlotSet(name,value) for name,value in graph_data.items()]
        else:
            dispatcher.utter_message(json.dumps({"graph_data": None, "message":message}))
        return events


class ActionChangeChartType(Action):

    def name(self) -> Text:
        return "action_change_chart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        events = []

        entities = {entity["entity"]: entity["value"] for entity in tracker.latest_message['entities']}
        slots = tracker.current_slot_values()

        is_available, message, slots = required_data_available(slots)

        if is_available:

            data_type = DataStorage.dataset_properties[slots["dataset"]]["data_type"]

            if data_type=="dataset":

                if "chart_type" in entities.keys():
                    chart_type = entities["chart_type"]
                else:
                    # TODO
                    return

                graph_data = slots
                graph_data["chart_type"] = chart_type
                graph_data["data_type"] = data_type

                dispatcher.utter_message(json.dumps({"graph_data":graph_data, "message": message}))

                events = [SlotSet("chart_type", entities["chart_type"]), SlotSet("data_type",data_type)]

            else:
                message = "This operation can not be applied to this data."
                dispatcher.utter_message(json.dumps({"graph_data": None, "message":message}))
        else:
            dispatcher.utter_message(json.dumps({"graph_data": None, "message":message}))
        return events




