import datetime, time, json
from sseclient import SSEClient as EventSource
from dateutil.parser import parse

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
        
def domain_report_task01(url, decreasing = True):
    """ 
        Generates report every minute on total changes made in Wikipedia Domains sorted in the order specified.
        An Infinite loop requiring keyboard interrupt.
    """
    count = 0
    dictt = {}
    curr = datetime.datetime.now();
    for event in EventSource(url):
        if event.event == 'message':
            try:
                change = json.loads(event.data)
            except ValueError:
                pass
            else:
                timee = parse(change['meta']['dt']); timee.isoformat(); timee = timee.replace(tzinfo = None)
                elapsed_time = divmod(abs((curr - timee).total_seconds()), 60) ## DIFFERENCE BETWEEN OF DATA RECEPTION TIME AND REPORT START TIME
                ## COLLECTING DATA UPTO 1 MINUTE
                if elapsed_time[0] < float(1):
                    count+=1
                    if change['meta']['domain'] in dictt.keys():
                        dictt[change['meta']['domain']] += 1
                    else:
                        dictt[change['meta']['domain']] = 1
                else:
                    break

    ## SORTING AND PRINTING THE REPORT
    print("\nTotal number of Wikipedia Domains Updated (in the last 1 minute):  ", count, "\n")
    sorted_dict = sort_dict(dictt, decreasing)
    for key in sorted_dict:
        print(key, ": ", sorted_dict[key], " pages updated")

def users_report_task01(url, show_anony = True, anony_count = False, decreasing = True):
    """
        Generates report every minute to give user names and their maximum edit count sorted in the order specified.
        An Infinite loop requiring keyboard interrupt.
    """
    dictt = {}
    anonymous_ip_count = 0
    curr = datetime.datetime.now();
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

                    timee = parse(change['meta']['dt']); timee.isoformat(); timee = timee.replace(tzinfo = None)
                    elapsed_time = divmod(abs((curr - timee).total_seconds()), 60) ## DIFFERENCE BETWEEN OF DATA RECEPTION TIME AND REPORT START TIME
                    ## COLLECTING DATA UPTO 1 MINUTE
                    if elapsed_time[0] < float(1):
                        if change['performer']['user_text'] in dictt.keys():
                            dictt[change['performer']['user_text']] = max(dictt[change['performer']['user_text']], change['performer']['user_edit_count'])
                        else:
                            dictt[change['performer']['user_text']] = change['performer']['user_edit_count']
                    else:
                        break
                except KeyError:
                    if show_anony:
                        dictt[change['performer']['user_text']] = -1
                    if anony_count:
                        anonymous_ip_count += 1

    ## SORTING AND PRINTING THE REPORT
    print("Users who made changes to en.wikipedia.org (in last 1 minute)")
    sorted_dict = sort_dict(dictt, decreasing)
    for key in sorted_dict:
        print(key, ": ", sorted_dict[key])
    ## PRINTING NUMBER OF ANONYMOUS IPs RECIEVED
    if(anony_count):
        print("Anonymous IP count: ", anonymous_ip_count)

def domain_report_bonus_task(url, decreasing = True):
    """
        Generates report of every minute for 5 minutes on total changes made in Wikipedia Domains sorted in the order specified.
        An Infinite loop requiring keyboard interrupt.
    """
    count = 0
    minute = 0
    dictt = {}
    curr = datetime.datetime.now();
    for event in EventSource(url):
        if event.event == 'message':
            try:
                change = json.loads(event.data)
            except ValueError:
                pass
            else:
                timee = parse(change['meta']['dt']); timee.isoformat(); timee = timee.replace(tzinfo = None)
                elapsed_time = divmod(abs((curr - timee).total_seconds()), 60) ## DIFFERENCE BETWEEN OF DATA RECEPTION TIME AND REPORT START TIME
                ## COLLECT DATA TILL 5 MINUTES
                if elapsed_time[0] < float(5):
                    ## PRINTING REPORT FOR THE Xth MINUTE IN SORTED ORDER
                    if elapsed_time[0]+(elapsed_time[1]/60.0) > float(minute+1):
                        sorted_dict = sort_dict(dictt, decreasing)
                        for key in sorted_dict:
                            print(key, ": ", sorted_dict[key], " pages updated in last ", minute+1, " minute(s)")
                        minute+=1

                    ## STORING USER DATA IN DICTIONARY
                    count+=1
                    if change['meta']['domain'] in dictt.keys():
                        dictt[change['meta']['domain']] += 1
                    else:
                        dictt[change['meta']['domain']] = 1
                else:
                    break
                    
    ## SORTING AND PRINTING THE REPORT
    print("\nTotal number of Wikipedia Domains Updated (in the last 5 minutes): ", count, "\n")
    sorted_dict = sort_dict(dictt, decreasing)
    for key in sorted_dict:
        print(key, ": ", sorted_dict[key], " pages updated in 5 minutes")
    
def users_report_bonus_task(url, show_anony = True, anony_count = False, decreasing = True):
    """
        Generates report every minute for 5 minutes to give user names and their maximum edit count sorted in the order specified.
        An Infinite loop requiring keyboard interrupt.
    """
    
    minute = 0
    dictt = {}
    anonymous_ip_count = 0
    curr = datetime.datetime.now();
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
                    
                    timee = parse(change['meta']['dt']); timee.isoformat(); timee = timee.replace(tzinfo = None)
                    elapsed_time = divmod(abs((curr - timee).total_seconds()), 60) ## DIFFERENCE BETWEEN OF DATA RECEPTION TIME AND REPORT START TIME
                    ## COLLECT DATA TILL 5 MINUTES
                    if elapsed_time[0] < float(5):
                        ## PRINTING REPORT FOR THE Xth MINUTE IN SORTED ORDER
                        if elapsed_time[0]+(elapsed_time[1]/60.0) > float(minute+1):
                            sorted_dict = sort_dict(dictt, decreasing)
                            for key in sorted_dict:
                                print(key, "updated in last ", minute+1, " minute(s)", "| Edit count: ", sorted_dict[key])
                            minute+=1

                        ## STORING USER DATA IN DICTIONARY
                        if change['performer']['user_text'] in dictt.keys():
                            dictt[change['performer']['user_text']] = max(dictt[change['performer']['user_text']], change['performer']['user_edit_count'])
                        else:
                            dictt[change['performer']['user_text']] = change['performer']['user_edit_count']
                    else:
                        break
                except KeyError:
                    ## CATCHING ANONYMOUS IP RECEIVED WITH NO "USER_EDIT_COUNT" PARAMETER
                    if show_anony:
                        dictt[change['performer']['user_text']] = -1
                    if anony_count:
                        anonymous_ip_count += 1
                    
    ## SORTING AND PRINTING THE REPORT
    print("\nUsers who made changes to en.wikipedia.org (in last 5 minutes)")
    sorted_dict = sort_dict(dictt, decreasing)
    for key in sorted_dict:
        print(key, ": ", sorted_dict[key])
    ## PRINTING NUMBER OF ANONYMOUS IPs RECIEVED
    if(anony_count):
        print("Anonymous IP count: ", anonymous_ip_count)

if __name__ == "__main__":
    show_anonymous = False
    anonymous_count = False
    while(True):
        try:
            response = int(input("\nEnter the required report:\n\t1. For domain report only for 1 minute\n\t\
2. For user report only for 1 minute\n\t3. For domain report of 5 minutes with minute-wise report\n\t\
4. For user report of 5 minutes with minute-wise report\n\tAny other number to exit code.\n"))
            if response == 1:

                domain_report_task01(url)

            elif response == 2:

                response_02 = str(input("Count anonymous IPs received: Y/N? "))
                anonymous_count = True if response_02 == 'Y' else False 
                response_02 = str(input("Show anonymous IPs received: Y/N? "))
                show_anonymous = True if response_02 == 'Y' else False

                users_report_task01(url, show_anony=show_anonymous, anony_count=anonymous_count)

            elif response == 3:

                domain_report_bonus_task(url)

            elif response == 4:

                response_02 = str(input("Count anonymous IPs received: Y/N? "))
                anonymous_count = True if response_02 == 'Y' else False 
                response_02 = str(input("Show anonymous IPs received: Y/N? "))
                show_anonymous = True if response_02 == 'Y' else False  

                users_report_bonus_task(url, show_anony=show_anonymous, anony_count=anonymous_count)

            else:

                print("Exiting code.")
                break

        except HTTPError:
            print("Please Try again")
