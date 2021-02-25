# ! pip install sseclient
import datetime, time, json, threading
from sseclient import SSEClient as EventSource
url = 'https://stream.wikimedia.org/v2/stream/revision-create'

def sort_dict(dictt, decreasing = True):
    """
        Sorts a dictionary in the order as indicated by the parameter "decreasing".
    """
    sorted_dict = {}
    sorted_keys = sorted(dictt, key=dictt.get, reverse=decreasing)
    for w in sorted_keys:
        sorted_dict[w] = dictt[w]
    return sorted_dict

def print_domain_report(dictt, decreasing=True):
    """
        Sorts and prints the data.
    """
    count = 0
    ## CHECKING IF ANY CHANGES RECEIVED VIA THE API
    if (not dictt):
        print("No changes made in the last 1 minute!")
    ## SORTING AND PRINTING THE REPORT
    else:
        sorted_dict = sort_dict(dictt, decreasing)
        for key in sorted_dict:
            print(key, ": ", sorted_dict[key], " pages updated")
            count+=sorted_dict[key]
        print("\nTotal number of Wikipedia Domains Updated (in the last 1 minute):  ", count, "\n")

def run_data(dictt):
    """
        Function to collect data for domain report.
    """
    for event in EventSource(url):
        if event.event == 'message':
            try:
                change = json.loads(event.data)
            except ValueError:
                pass
            else:
                if change['meta']['domain'] in dictt.keys():
                    dictt[change['meta']['domain']] += 1
                else:
                    dictt[change['meta']['domain']] = 1
        global stop_threads 
        if stop_threads: 
            break
    return dictt

def count_time(sec):
    """
        Utility function to stop trigger print of reports.
    """
    time.sleep(sec)
    global stop_threads
    stop_threads = True

##_______________________________________________________________________________________________________________________________________________________________________________________________________________________________


def run_user(dictt):
    """
        Function to collect data for user reports.
    """
    for event in EventSource(url):
        if event.event == 'message':
            try:
                change = json.loads(event.data)
            except ValueError:
                pass
            else:
                try:
                    ## CHECK IF USER IS A BOT OR THE DOMAIN IS NOT "en.wikipedia.org". DO NOT COLLECT DATA IF EITHER IS TRUE.
                    if change['meta']['domain'] != "en.wikipedia.org" or change['performer']['user_is_bot']:
                        continue

                    ## COLLECTING DATA UPTO 1 MINUTE
                    if change['performer']['user_text'] in dictt.keys():
                        dictt[change['performer']['user_text']] = max(dictt[change['performer']['user_text']], change['performer']['user_edit_count'])
                    else:
                        dictt[change['performer']['user_text']] = change['performer']['user_edit_count']
                    
                except KeyError:
                    dictt[change['performer']['user_text']] = -1
        global stop_threads 
        if stop_threads: 
            break
    return dictt

def print_user_report(dictt, decreasing=True):
    """
        Sorts and prints the data.
    """
    anonymous_ip_count = 0
    ## CHECKING IF ANY CHANGES RECEIVED VIA THE API
    if (not dictt):
        print("No changes made in the last 1 minute!")
    ## SORTING AND PRINTING THE REPORT
    else:
        print("Users who made changes to en.wikipedia.org (in last 1 minute)")
        sorted_dict = sort_dict(dictt, decreasing)
        for key in sorted_dict:
            print(key, ": ", sorted_dict[key])
            if (sorted_dict[key] == -1):
                anonymous_ip_count +=1
        ## PRINTING NUMBER OF ANONYMOUS IPs RECIEVED
        print("Anonymous IP count: ", anonymous_ip_count)

##_______________________________________________________________________________________________________________________________________________________________________________________________________________________________

def mergeDictsOverwriteSum(d1, d2):
    """
        Helper function.
    """
    res = d2.copy()
    if (not d1):
        return d2
    elif (not d2):
        return d1
    else:
        for k,v in d1.items():
            if k in d2:
                res[k] = d2[k] + v
            else:
                res[k] = v
        return res

def merge_nest_dict(dictt):
    """
        Helper function.
    """
    dict_new = {}
    for i, _ in dictt.items():
        dict_new = mergeDictsOverwriteSum(dict_new, dictt[i])
    return dict_new

def sort_nest_dict(dictt, decreasing = True):
    """
        Merges a nested dictionary to a dictionary and then sorts in the order as indicated by the parameter "decreasing".
    """
    dict_new = merge_nest_dict(dictt)
    sorted_dict = {}
    sorted_keys = sorted(dict_new, key=dict_new.get, reverse=decreasing)
    for w in sorted_keys:
        sorted_dict[w] = dict_new[w]
    return sorted_dict

## _______________________________________________________________________________________________________________________________

def print_domain_report_bonus(dictt, minute, decreasing=True):
    """
        Prints domain report of bonus task.
    """
    ## SORTING AND PRINTING THE REPORT                
    count = 0
    sorted_dict = sort_nest_dict(dictt, decreasing)
    for key in sorted_dict:
        print(key, ": ", sorted_dict[key]," pages updated.")
        count += sorted_dict[key]
    print("\nTotal number of Wikipedia Domains Updated (from %d to %d minutes): %d\n"%(max(minute-5,0), minute, count))

def run_data_bonus(dictt):
    """
        Collects domain data for bonus task.
    """
    global minute
    min = minute
    for event in EventSource(url):
        if event.event == 'message':
            try:
                change = json.loads(event.data)
            except ValueError:
                pass
            else:
            ## STORING USER DATA IN DICTIONARY
                if change['meta']['domain'] in dictt[(min%5)].keys():
                    dictt[(min%5)][change['meta']['domain']] += 1
                else:
                    dictt[(min%5)][change['meta']['domain']] = 1
        global stop_threads 
        if stop_threads: 
            break
        
##_______________________________________________________________________________________________________________________________________________________________________________________________________________________________

def mergeDictsOverwriteMax(d1, d2):
    """
        Helper function.
    """
    res = d2.copy()
    if (not d1):
        return d2
    elif (not d2):
        return d1
    for k,v in d1.items():
        if k in d2:
            res[k] = max(d2[k], v)
        else:
            res[k] = v
    return res

def merge_nest_dict_user(dictt):
    """
        Helper function.
    """
    dict_new = {}
    for i, _ in dictt.items():
        dict_new = mergeDictsOverwriteMax(dict_new, dictt[i])
    return dict_new

def sort_nest_dict_user(dictt, decreasing=True):
    """
        Merges a nested dictionary to a dictionary and then sorts in the order as indicated by the parameter "decreasing".
    """
    dict_new = merge_nest_dict_user(dictt)
    sorted_dict = {}
    sorted_keys = sorted(dict_new, key=dict_new.get, reverse=decreasing)
    for w in sorted_keys:
        sorted_dict[w] = dict_new[w]
    return sorted_dict

## ________________________________________________________________________________________________________________________________

def print_user_report_bonus(dictt, minute, decreasing = True):
    """
        Prints user report of bonus task.
    """
    anonymous_ip_count = 0
    print("\nUsers who made changes to en.wikipedia.org (from %d to %d minutes)\n"%(max(minute-5,0), minute))
    sorted_dict = sort_nest_dict_user(dictt, decreasing)
    for key in sorted_dict:
        print(key, ": ", sorted_dict[key])
        if (sorted_dict[key] == -1):
                anonymous_ip_count +=1
    ## PRINTING NUMBER OF ANONYMOUS IPs RECIEVED
    print("Anonymous IP count: ", anonymous_ip_count)


def run_user_bonus(dictt):
    """
        Collects user data for bonus task.
    """
    global minute
    min = minute
    for event in EventSource(url):
        if event.event == 'message':
            try:
                change = json.loads(event.data)
            except ValueError:
                pass
            else:
                try:
                    ## CHECK IF USER IS A BOT OR THE DOMAIN IS NOT "en.wikipedia.org". DO NOT COLLECT DATA IF EITHER IS TRUE.
                    if change['meta']['domain'] != "en.wikipedia.org" or change['performer']['user_is_bot']:
                        continue

                    ## STORING USER DATA IN DICTIONARY
                    if change['performer']['user_text'] in dictt[(min%5)].keys():
                        dictt[(min%5)][change['performer']['user_text']] = max(dictt[(min%5)][change['performer']['user_text']], change['performer']['user_edit_count'])
                    else:
                        dictt[(min%5)][change['performer']['user_text']] = change['performer']['user_edit_count']
                        
                except KeyError:
                    ## CATCHING ANONYMOUS IP RECEIVED WITH NO "USER_EDIT_COUNT" PARAMETER
                    dictt[(min%5)][change['performer']['user_text']] = -1
        global stop_threads 
        if stop_threads: 
            break


##_______________________________________________________________________________________________________________________________________________________________________________________________________________________________

if __name__ == "__main__":

    sec = 60 ## 60 for minute wise report

    while(True):
        try:
            response = int(input("\nEnter the required report:\n\t1. For domain report only for 1 minute\n\t\
2. For user report only for 1 minute\n\t3. For domain report of past 5 minutes with minute-wise report\n\t\
4. For user report of past 5 minutes with minute-wise report\n\tAny other number to exit code.\n"))
            
            if response == 1:

                dictt = {}
                stop_threads = False
                t1 = threading.Thread(target = run_data, kwargs= dict (dictt=dictt))
                t2 = threading.Thread(target = count_time, kwargs=dict (sec=sec))
                t1.start(); t2.start()
                t1.join(); t2.join()

                print_domain_report(dictt)

            elif response == 2:

                dictt = {}
                stop_threads = False
                t1 = threading.Thread(target = run_user, kwargs= dict (dictt=dictt))
                t2 = threading.Thread(target = count_time, kwargs=dict (sec=sec))
                t1.start(); t2.start()
                t1.join(); t2.join()

                print_user_report(dictt)

            elif response == 3:

                dictt = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}}
                minute = 0
                while (True):
                    dictt[(minute%5)] = {}
                    stop_threads = False
                    t1 = threading.Thread(target = run_data_bonus, kwargs= dict (dictt=dictt))
                    t2 = threading.Thread(target = count_time, kwargs=dict (sec=sec))
                    t1.start(); t2.start()
                    t1.join(); t2.join()
                    minute += 1

                    print_domain_report_bonus(dictt, minute)

            elif response == 4:

                dictt = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}}
                minute = 0
                while (True):
                    dictt[(minute%5)] = {}
                    stop_threads = False
                    t1 = threading.Thread(target = run_user_bonus, kwargs= dict (dictt=dictt))
                    t2 = threading.Thread(target = count_time, kwargs=dict (sec=sec))
                    t1.start(); t2.start()
                    t1.join(); t2.join()
                    minute += 1

                    print_user_report_bonus(dictt, minute)

            else:

                print("Exiting code.")
                break

        except HTTPError:
            print("Please Try again")
