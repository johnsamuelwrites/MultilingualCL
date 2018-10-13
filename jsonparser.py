import json

alias={}
alias["en_US"] = "alias"

# resources and their labels in different languages
user_label = {}
user_label["en_US"] = ["user"]

group_label = {}
group_label["en_US"] = ["group"]

process_label = {}
process_label["en_US"] = ["process"]

memory_label = {}
memory_label["en_US"] = ["memory"]

device_label = {}
device_label["en_US"] = ["device"]

connection_label = {}
connection_label["en_US"] = ["connection"]

file_label = {}
file_label["en_US"] = ["file"]

directory_label = {}
directory_label["en_US"] = ["directory"]

date_label = {}
date_label["en_US"] = ["date"]

option={}
option["en_US"] = "option"

command = {}
command["en_US"] = {}
command["en_US"]["create"] = {}
command["en_US"]["create"][alias["en_US"]] = ["make"]
command["en_US"]["create"][option["en_US"]] = [
        user_label["en_US"][0],
        group_label["en_US"][0],
        file_label["en_US"][0],
        directory_label["en_US"][0]]

command["en_US"]["read"] = {}
command["en_US"]["read"][alias["en_US"]] = ["show", "print"]
command["en_US"]["read"][option["en_US"]] = [
        user_label["en_US"][0],
        date_label["en_US"][0],
        group_label["en_US"][0],
        process_label["en_US"][0],
        file_label["en_US"][0],
        directory_label["en_US"][0]]

command["en_US"]["update"] = {}
command["en_US"]["update"][alias["en_US"]] = []
command["en_US"]["update"][option["en_US"]] = [
        user_label["en_US"][0],
        group_label["en_US"][0],
        file_label["en_US"][0],
        directory_label["en_US"][0]]

command["en_US"]["delete"] = {}
command["en_US"]["delete"][alias["en_US"]] = []
command["en_US"]["delete"][option["en_US"]] = [
        user_label["en_US"][0],
        group_label["en_US"][0],
        process_label["en_US"][0],
        file_label["en_US"][0],
        directory_label["en_US"][0]]

command["en_US"]["list"] = {}
command["en_US"]["list"][alias["en_US"]] = []
command["en_US"]["list"][option["en_US"]] = [
        user_label["en_US"][0],
        memory_label["en_US"][0],
        device_label["en_US"][0],
        group_label["en_US"][0],
        process_label["en_US"][0],
        connection_label["en_US"][0],
        file_label["en_US"][0],
        directory_label["en_US"][0]]

command["en_US"]["compress"] = {}
command["en_US"]["compress"][alias["en_US"]] = []
command["en_US"]["compress"][option["en_US"]] = [
        file_label["en_US"][0],
        directory_label["en_US"][0]]

command["en_US"]["decompress"] = {}
command["en_US"]["decompress"][alias["en_US"]] = []
command["en_US"]["decompress"][option["en_US"]] = [
        file_label["en_US"][0],
        directory_label["en_US"][0]]

command["en_US"]["link"] = {}
command["en_US"]["link"][option["en_US"]] = [
        file_label["en_US"][0],
        directory_label["en_US"][0]]

command["en_US"]["copy"] = {}
command["en_US"]["copy"][option["en_US"]] = [
        file_label["en_US"][0],
        directory_label["en_US"][0]]

command["en_US"]["rename"] = {}
command["en_US"]["rename"][option["en_US"]] = [
        file_label["en_US"][0],
        directory_label["en_US"][0]]

print(json.dumps(command, indent=4))
