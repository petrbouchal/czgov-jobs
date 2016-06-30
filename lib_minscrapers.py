__author__ = 'petrbouchal'

def open_withcookies(urltouse):
    import urllib2
    import cookielib

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    request = urllib2.Request(url=urltouse, headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'})
    r = opener.open(request)
    return r

def open_checksnag(urltouse):
    import urllib2
    try:
        response = open_withcookies(urltouse)
    except urllib2.HTTPError as e:
        # print(e)
        if e.getcode() == 302 and e.headers.get('Location') is not None:
            opener = urllib2.build_opener()
            cookie = e.headers.get('Set-Cookie')
            # print(cookie)
            opener.addheaders.append(('Cookie', cookie))
            opener.addheaders.append(('User-agent', 'Mozilla/5.0 (Linux i686)'))
            newurl = e.headers.get('Location')
            # print(newurl)
            response = opener.open(newurl)
            return response
        else:
            print('Error opening page')
            raise
    return response

def completeurl(fullurl, partialurl):
    from urllib2 import urlparse
    parsed_jobsurl = urlparse.urlparse(fullurl)
    parsed_joburl = urlparse.urlparse(partialurl)
    fulljoburl = urlparse.urlunparse([parsed_jobsurl.scheme, parsed_jobsurl.netloc,
                                      parsed_joburl.path, parsed_joburl.params, parsed_joburl.query,
                                      parsed_joburl.fragment])
    return fulljoburl


def scrapejobs(timestamp, bodydata):
    from bs4 import BeautifulSoup

    print(bodydata['jobsurl'])
    import urlparse
    import re

    page = open_checksnag(bodydata['jobsurl'])
    page = page.read()
    # print(page)
    page = BeautifulSoup(page, "html.parser")
    jobslist = []

    jobs = page.select(bodydata['jobtitledata']['itemselect'])
    # for i in jobs: print(i.contents)

    # Add href attribute if URL was collected separately
    if bodydata['separateurl']:
        joburls = page.select(bodydata['joburldata']['itemselect'])
        for count in range(0, len(jobs), 1):
            jobs[count].attrs['href'] = joburls[count]['href']

    # Add additional title text if it is to be collected
    if bodydata['jobtitledata']['additionaltitletext']:
        additionaltexts = page.select(bodydata['jobtitledata']['additionaltextselect'])
        for count in range(0, len(jobs), 1):
            jobs[count].contents = jobs[count].contents[0].strip() + ', ' + additionaltexts[count].contents[0].strip()
    else:
        for job in jobs: job.contents = job.contents[0].strip()

    for job in jobs:
        fulljoburl = completeurl(bodydata['jobsurl'], job['href'])
        if bodydata['abbrev'] == 'MSp': fulljoburl = bodydata['jobsurl']  # to get around session-dependent MSp pages
        jobtitle = re.sub('([\w])', lambda x: x.groups()[0].upper(), job.contents, 1, flags=re.UNICODE)
        jobdict = {'joburl': fulljoburl, 'jobtitle': jobtitle, 'dept': bodydata['abbrevcz'], 'datetime': timestamp}
        jobslist.append(jobdict)
    # print(jobslist)
    return jobslist


def scrapepages(timestamp, bodydata):
    from bs4 import BeautifulSoup

    jobsurlslist = [bodydata['jobsurl']]
    jobspageurl_iter = bodydata['jobsurl']

    def getnextlink(bodydata, iterfirsturl):
        if(bodydata['paginate'] == False):
            return False
        else:
            iterpage = open_checksnag(iterfirsturl)
            iterpage = iterpage.read()
            itersoup = BeautifulSoup(iterpage, "html.parser")
            nextlink = itersoup.select(bodydata['paginatelinkselect'])
            if len(nextlink) == 0:
                return False
            else:
                nextlink_final = completeurl(bodydata['jobsurl'],nextlink[0]['href'])
                return nextlink_final

    while (getnextlink(bodydata, jobspageurl_iter)):
        jobsurlslist.append(getnextlink(bodydata, jobspageurl_iter))
        # use the next link on each new page, but only if the next link differs from the previous one
        # this is because on some pages the next link remains active even on the last page
        if((jobsurlslist[-1]==getnextlink(bodydata, jobspageurl_iter)) & (bodydata['abbrev']=="MMR")):
            break # restrict the non-repeat rule to MMR because in MV they do repeat but it works
        else:
            jobspageurl_iter = getnextlink(bodydata, jobspageurl_iter)

    alljobslist = []
    for jobspageurl in jobsurlslist:
        newbodydata = bodydata
        newbodydata['jobsurl'] = jobspageurl
        thispagejoblist = scrapejobs(timestamp, newbodydata)
        alljobslist = alljobslist + thispagejoblist

    print('Nalezeno ' + str(len(alljobslist)) + ' pozic na ' + str(bodydata['abbrevcz']))

    return alljobslist
