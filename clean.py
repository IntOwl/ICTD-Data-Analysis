import pickle
import lzma
import pprint
import datetime
import numpy as np
import multiprocessing as mp
import lzma

userlogs = dict()
syslogs = dict()

def save_as_fast_flowlog(day, log_type):
    with open("data/weeks/%ss/%s-%s.pickle" % (log_type, log_type, day), mode="rb") as f:
        flowlog = pickle.load(f)
    count = 0
    for entry in flowlog:
        count += 1
    numpy_flowlog = np.empty([count, 1], dtype='u4, u4, datetime64[s], u4, u4, U64, U64, datetime64[s], u1')
    index = 0
    for entry in flowlog:
        numpy_flowlog[index][0][0] = entry['bytes_a_to_b']
        numpy_flowlog[index][0][1] = entry['bytes_b_to_a']
        numpy_flowlog[index][0][2] = np.datetime64(entry['end_time'])
        numpy_flowlog[index][0][3] = entry['port_a']
        numpy_flowlog[index][0][4] = entry['port_b']
        if 'private_addr' in entry.keys():
            numpy_flowlog[index][0][5] = entry['private_addr']
        elif 'address_a' in entry.keys():
            numpy_flowlog[index][0][5] = str(entry['address_a'])
            numpy_flowlog[index][0][6] = str(entry['address_b'])
        elif 'obfuscated_a' in entry.keys():
            numpy_flowlog[index][0][5] = entry['obfuscated_a']
            numpy_flowlog[index][0][6] = entry['obfuscated_b']
        else:
            print(entry)
        if 'public_addr' in entry.keys():
            numpy_flowlog[index][0][6] = str(entry['public_addr'])
        else:
            print(entry)
        numpy_flowlog[index][0][7] = np.datetime64(entry['start_time'])
        numpy_flowlog[index][0][8] = entry['transport_protocol']
        index += 1
    return numpy_flowlog

def save_as_fast_syslog(day):
    with open("data/weeks/syslogs/syslog-%s.pickle" % day, mode="rb") as f:
        syslog = pickle.load(f)
    count = 0
    for entry in syslog:
        count += 1
    numpy_syslog = np.empty([count, 1], dtype='U15, U15, u4, u4, datetime64[s], u4, u4, datetime64[s], u1')
    index = 0
    for entry in syslog:
        numpy_syslog[index][0][0] = entry['address_a']
        numpy_syslog[index][0][1] = entry['address_b']
        numpy_syslog[index][0][2] = entry['bytes_a_to_b']
        numpy_syslog[index][0][3] = entry['bytes_b_to_a']
        numpy_syslog[index][0][4] = np.datetime64(entry['end_time'])
        numpy_syslog[index][0][5] = entry['port_a']
        numpy_syslog[index][0][6] = entry['port_b']
        numpy_syslog[index][0][7] = np.datetime64(entry['start_time'])
        numpy_syslog[index][0][8] = entry['transport_protocol']
        index += 1
    return numpy_syslog

def clean_and_store_fast():
    dates = list()
    for i in range((datetime.date(2019, 5, 17) - datetime.date(2019, 3, 4)).days + 1):
        dates.append(datetime.date(2019, 3, 4) + datetime.timedelta(days=i))
    for date in dates:
        print(date)
        flowlog = save_as_fast_flowlog(str(date), "flowlog")
        local_userlog = save_as_fast_flowlog(str(date), "local_userlog")
        remote_userlog = save_as_fast_flowlog(str(date), "remote_userlog")
        np.save("data/numpy/userlogs", flowlog)
        np.save("data/numpy/userlogs", remote_userlog)
        np.save("data/numpy/userlogs", local_userlog)
        syslog = save_as_fast_syslog(str(date))
        np.save("data/numpy/syslogs", syslog)

def clean_and_store(day):
    logs = extract_small(day)
    flowlog = logs[0]
    syslog = logs[1]
    remote_userlog = list()
    local_userlog = list()
    netbios_log = list()
    for entry in flowlog:
        if 'public_addr' in entry.keys() and str(entry['public_addr']) == '192.168.151.1':
            local_userlog.append(entry)
        elif 'obfuscated_a' in entry.keys() and 'obfuscated_b' in entry.keys():
            netbios_log.append(entry)
        else:
            remote_userlog.append(entry)
    with open("data/weeks/flowlogs/flowlog-%s.pickle" % day, mode="wb") as f:
        pickle.dump(flowlog, f, protocol=pickle.HIGHEST_PROTOCOL)
    with open("data/weeks/remote_userlogs/remote_userlog-%s.pickle" % day, mode="wb") as g:
        pickle.dump(remote_userlog, g, protocol=pickle.HIGHEST_PROTOCOL)
    with open("data/weeks/local_userlogs/local_userlog-%s.pickle" % day, mode="wb") as h:
        pickle.dump(local_userlog, h, protocol=pickle.HIGHEST_PROTOCOL)
    with open("data/weeks/syslogs/syslog-%s.pickle" % day, mode="wb") as i:
        pickle.dump(syslog, i, protocol=pickle.HIGHEST_PROTOCOL)
    with open("data/weeks/netbios/netbios-%s.pickle" % day, mode="wb") as j:
        pickle.dump(netbios_log, j, protocol=pickle.HIGHEST_PROTOCOL)

def split_by_dates(filename): # run once
    with lzma.open(filename) as f:
        current = pickle.load(f)
        date = (current['start_time'] + datetime.timedelta(hours=9)).date()
        prev_date = (current['start_time'] + datetime.timedelta(hours=9)).date()
        date_dicts = list()
        while True:
            if (date != prev_date):
                with open("data/%s.pickle" % str(prev_date), mode="wb") as g:
                    for entry in date_dicts:
                        pickle.dump(entry, g, protocol=pickle.HIGHEST_PROTOCOL)
                    date_dicts = list()
            prev_date = (current['start_time'] + datetime.timedelta(hours=9)).date()
            try:
                current = pickle.load(f)
                date_dicts.append(current)
                date = (current['start_time'] + datetime.timedelta(hours=9)).date()
            except EOFError:
                break
        with open("data/%s.pickle" % str(date), mode="wb") as g:
            for entry in date_dicts:
                pickle.dump(entry, g, protocol=pickle.HIGHEST_PROTOCOL)
            date_dicts = list()

def split_by_weeks(filename): # run once
    with lzma.open(filename) as f:
        current = pickle.load(f)
        date = (current['start_time'] + datetime.timedelta(hours=9)).date()
        prev_date = (current['start_time'] + datetime.timedelta(hours=9)).date()
        date_dicts = list()
        while True:
            print(date)
            print(prev_date)
            if (date > prev_date + datetime.timedelta(days=6)):
                for i in range(20):
                    print("CHANGING")
                with open("data/weeks/%s.pickle" % str(prev_date), mode="wb") as g:
                    for entry in date_dicts:
                        pickle.dump(entry, g, protocol=pickle.HIGHEST_PROTOCOL)
                date_dicts = list()
                prev_date = (current['start_time'] + datetime.timedelta(hours=9)).date()
            try:
                current = pickle.load(f)
                date_dicts.append(current)
                date = (current['start_time'] + datetime.timedelta(hours=9)).date()
            except EOFError:
                break
        with open("data/weeks/%s.pickle" % str(date), mode="wb") as g:
            for entry in date_dicts:
                pickle.dump(entry, g, protocol=pickle.HIGHEST_PROTOCOL)
            date_dicts = list()

def extract_small(day):
    flowlog = list()
    syslog = list()
    with open("data/weeks/weeklog-%s.pickle" % day, mode="rb") as f:
        flowlog.append(pickle.load(f))
        old_index = 0
        oldest = flowlog[0]
        cont = True
        temp = oldest
        # print(temp)
        while cont:
            temp['start_time'] = temp['start_time'] + datetime.timedelta(hours=9)
            temp['end_time'] = temp['end_time'] + datetime.timedelta(hours=9)
            try:
                if temp['start_time'] == oldest['end_time']: # checking for following 5-tuple
                    # not swapped
                    if temp['port_a'] == oldest['port_a'] and temp['port_b'] == oldest['port_b'] and temp['transport_protocol'] == oldest['transport_protocol']: # checking for port matches:
                        if ('obfuscated_a' in oldest.keys() 
                            and 'obfuscated_a' in temp.keys() and oldest['obfuscated_a'] == temp['obfuscated_a']) or ('obfuscated_b' in oldest.keys() and 'obfuscated_b' in temp.keys() 
                                                                                                                    and oldest['obfuscated_b'] == temp['obfuscated_b']):
                            #combine
                            oldest['bytes_b_to_a'] += temp['bytes_b_to_a']
                            oldest['bytes_a_to_b'] += temp['bytes_a_to_b']
                            old_index += 1
                            oldest = flowlog[old_index]
                    elif temp['port_a'] == oldest['port_b'] and temp['port_b'] == oldest['port_a']: # checking for port matches:
                        if ('obfuscated_a' in oldest.keys() and 'obfuscated_b' in temp.keys() # swapped
                        and oldest['obfuscated_a'] == temp['obfuscated_b']):
                            #combine
                            oldest['bytes_b_to_a'] += temp['bytes_a_to_b']
                            oldest['bytes_a_to_b'] += temp['bytes_b_to_a']
                            old_index += 1
                            oldest = flowlog[old_index]
                        elif ('obfuscated_b' in oldest.keys() and 'obfuscated_a' in temp.keys() # swapped the other way
                        and oldest['obfuscated_b'] == temp['obfuscated_a']):
                            # combine
                            oldest['bytes_b_to_a'] += temp['bytes_a_to_b']
                            oldest['bytes_a_to_b'] += temp['bytes_b_to_a']
                            # change previous addresses/ports
                            oldest['obfuscated_a'] = temp['obfuscated_a']
                            oldest['address_b'] = temp['address_b']
                            oldest['port_a'] = temp['port_b']
                            oldest['port_b'] = temp['port_a']
                            # get rid of old addresses
                            oldest.pop('obfuscated_b')
                            oldest.pop('address_a')
                            old_index += 1
                            oldest = flowlog[old_index]
                elif temp['start_time'] > oldest['end_time']:
                    while (temp['start_time'] > oldest['end_time']) and (old_index + 1 < len(flowlog)):
                        old_index += 1
                        oldest = flowlog[old_index]
                if 'obfuscated_a' in temp.keys() or 'obfuscated_b' in temp.keys():
                    flowlog.append(temp)
                else:
                    syslog.append(temp)
                temp = pickle.load(f)
            except EOFError:
                cont = False
    for entry in flowlog:
        entry = remove_obfuscated(entry)
    return flowlog, syslog

def remove_obfuscated(temp):
    if 'obfuscated_a' in temp.keys():
        if 'obfuscated_b' in temp.keys():
            if temp['port_b'] == 137 or temp['port_a'] == 137:
                print(temp)   
        else:
            temp['public_addr'] = temp['address_b']
            temp.pop('address_b')
            temp['private_addr'] = temp['obfuscated_a']
            temp.pop('obfuscated_a')
    elif 'obfuscated_b' in temp.keys():
        temp['private_addr'] = temp['obfuscated_b']
        temp['public_addr'] = temp['address_a']
        temp.pop('obfuscated_b')
        temp.pop('address_a')
        port_b = temp['port_a']
        temp['port_a'] = temp['port_b']
        temp['port_b'] = port_b
        bytes_b_to_a = temp['bytes_b_to_a']
        temp['bytes_b_to_a'] = temp['bytes_a_to_b']
        temp['bytes_a_to_b'] = bytes_b_to_a
    return temp

def load_day(day):
    with open("data/flowlogs/flowlog-%s.pickle" % day, mode="rb") as f:
        flowlog = pickle.load(f)
    with open("data/local_userlogs/local_userlog-%s.pickle" % day, mode="rb") as g:
        local_userlog = pickle.load(g)
    with open("data/remote_userlogs/remote_userlog-%s.pickle" % day, mode="rb") as h:
        remote_userlog = pickle.load(h)
    with open("data/syslogs/syslog-%s.pickle" % day, mode="rb") as j:
        syslog = pickle.load(j)
    userlogs[day] = (flowlog, remote_userlog, local_userlog)
    syslogs[day] = syslog
    return day, (flowlog, remote_userlog, local_userlog), syslog

if __name__ == '__main__':
    dates = list()
    for i in range((datetime.date(2019, 5, 13) - datetime.date(2019, 3, 4)).days + 1):
        if i % 7 == 0:
            dates.append(datetime.date(2019, 3, 4) + datetime.timedelta(days=i))
    # for date in dates:
    #     print(date)
    #     with open("data/weeks/remote_userlogs/remote_userlog-%s.pickle" % str(date), mode="rb") as d:
    #         temp = pickle.load(d)
    #     with lzma.open("data/weeks/remote_userlogs/%s.xz" % str(date), mode="wb") as f:
    #         for entry in temp:
    #             f.write(entry)
    for date in dates:
        remote_userlog = save_as_fast_flowlog(str(date), 'remote_userlog')
        local_userlog = save_as_fast_flowlog(str(date), 'local_userlog')
        netbios = save_as_fast_flowlog(str(date), 'netbios')
        syslog = save_as_fast_syslog(str(date))
        with open("data/numpy/remote_userlogs/%s.npy" % str(date), mode="wb") as g:
            for entry in remote_userlog:
                pickle.dump(entry, g, protocol = pickle.HIGHEST_PROTOCOL)
        with open("data/numpy/local_userlogs/%s.npy" % str(date), mode="wb") as h:
            for entry in local_userlog:
                pickle.dump(entry, h, protocol = pickle.HIGHEST_PROTOCOL)
        with open("data/numpy/netbios/%s.npy" % str(date), mode="wb") as i:
            for entry in netbios:
                pickle.dump(entry, i, protocol = pickle.HIGHEST_PROTOCOL)
        with open("data/numpy/syslogs/%s.npy" % str(date), mode="wb") as j:
            for entry in syslog:
                pickle.dump(entry, j, protocol = pickle.HIGHEST_PROTOCOL)
    # dates = list()
    # for i in range((datetime.date(2019, 5, 17) - datetime.date(2019, 3, 4)).days + 1):
    #     dates.append(datetime.date(2019, 3, 4) + datetime.timedelta(days=i))
    # userlogs = dict()
    # for date in dates:
    #     clean_and_store(date)
    #     print(date)
    # split_by_dates('data/2019-05-17-flowlog_archive-000.xz')

    # dates = list()
    # i = datetime.date(2019, 3, 4)
    # week = list()
    # while (i < datetime.date(2019, 5, 17)):
    #     with open("data/weeks/weeklog-%s.pickle" % str(i), mode="rb") as f:
    #         while True:
    #             try:
    #                 week.append(pickle.load(f))
    #             except EOFError:
    #                 break
    #         print(week)
    #         for entry in week:
    #             entry['start_time'] += datetime.timedelta(hours=9)
    #             entry['end_time'] += datetime.timedelta(hours=9)
    #     with open("data/weeks/weeklog-%s.pickle" % str(i), mode="wb") as g:
    #         for entry in week:
    #             pickle.dump(week, g, protocol=pickle.HIGHEST_PROTOCOL)
    #     week = list()
    #     i += datetime.timedelta(days=7)
    # for i in range((datetime.date(2019, 5, 17) - datetime.date(2019, 3, 4)).days + 1):
    #     dates.append(str(datetime.date(2019, 3, 4) + datetime.timedelta(days=i)))
    # week = list()
    # for date in dates:
    #     if len(week) == 7:
    #         split_by_weeks(week)
    #         week = list()
    #     print(date)
    #     week.append(date)

    # dates = list()
    # for i in range((datetime.date(2019, 3, 10) - datetime.date(2019, 3, 4)).days + 1):
    #     dates.append(str(datetime.date(2019, 3, 4) + datetime.timedelta(days=i)))
    # split_by_weeks(dates)
