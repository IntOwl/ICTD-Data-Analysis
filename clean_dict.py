import pickle

def clean_dnslog(filename):
    with open(filename, mode="rb") as f:
        dnslog = pickle.load(f)
    new_dnslog = dict()
    # sorting through the dnslog dict to create a new dict (new_dnslog) with each key being the site name 
    # and each value being a list of all the urls for that site
    for entry in dnslog:
        if 'google' in dnslog[entry] or 'gmail' in dnslog[entry]:
            if 'google' not in new_dnslog:
                new_dnslog['google'] = list()
            if dnslog[entry] not in new_dnslog['google']:
                new_dnslog['google'].append(dnslog[entry])
        elif 'fbcdn' in dnslog[entry] or 'facebook' in dnslog[entry] or 'fbsbx' in dnslog[entry]:
            if 'facebook' not in new_dnslog:
                new_dnslog['facebook'] = list()
            if dnslog[entry] not in new_dnslog['facebook']:
                new_dnslog['facebook'].append(dnslog[entry])
        elif 'whatsapp' in dnslog[entry]:
            if 'whatsapp' not in new_dnslog:
                new_dnslog['whatsapp'] = list()
            if dnslog[entry] not in new_dnslog['whatsapp']:
                new_dnslog['whatsapp'].append(dnslog[entry])
        elif 'twimg' in dnslog[entry] or 'twitter' in dnslog[entry]:
            if 'twitter' not in new_dnslog:
                new_dnslog['twitter'] = list()
            if dnslog[entry] not in new_dnslog['twitter']:
                new_dnslog['twitter'].append(dnslog[entry])
        elif 'instagram' in dnslog[entry]:
            if 'instagram' not in new_dnslog:
                new_dnslog['instagram'] = list()
            if dnslog[entry] not in new_dnslog['instagram']:
                new_dnslog['instagram'].append(dnslog[entry])
        elif 'ytimg' in dnslog[entry] or 'youtube' in dnslog[entry]:
            if 'youtube' not in new_dnslog:
                new_dnslog['youtube'] = list()
            if dnslog[entry] not in new_dnslog['youtube']:
                new_dnslog['youtube'].append(dnslog[entry])
        elif 'wikipedia' in dnslog[entry]:
            if 'wikipedia' not in new_dnslog:
                new_dnslog['wikipedia'] = list()
            if dnslog[entry] not in new_dnslog['wikipedia']:
                new_dnslog['wikipedia'].append(dnslog[entry])
        elif 'akamai' in dnslog[entry]:
            if 'akamai cdn' not in new_dnslog:
                new_dnslog['akamai cdn'] = list()
            if dnslog[entry] not in new_dnslog['akamai cdn']:
                new_dnslog['akamai cdn'].append(dnslog[entry])
        elif 'amazonaws' in dnslog[entry] or 'aws' in dnslog[entry]:
            if 'amazon cdn' not in new_dnslog:
                new_dnslog['amazon cdn'] = list()
            if dnslog[entry] not in new_dnslog['amazon cdn']:
                new_dnslog['amazon cdn'].append(dnslog[entry])
        elif 'cloudfront' in dnslog[entry]:
            if 'cloudfront cdn' not in new_dnslog:
                new_dnslog['cloudfront cdn'] = list()
            if dnslog[entry] not in new_dnslog['cloudfront cdn']:
                new_dnslog['cloudfront cdn'].append(dnslog[entry])
        elif 'cloudflare' in dnslog[entry]:
            if 'cloudflare cdn' not in new_dnslog:
                new_dnslog['cloudflare cdn'] = list()
            if dnslog[entry] not in new_dnslog['cloudflare cdn']:
                new_dnslog['cloudflare cdn'].append(dnslog[entry])

    with open('data/oaxaca_dnslog.pickle', mode="wb") as g:
        pickle.dump(new_dnslog, g, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    clean_dnslog('data/dnslog.pickle')