import urllib2
import sys
import bs4
import re

user_name = sys.argv[1]
password =  sys.argv[2]

print "Username: ", user_name
print "Password: ", password[0] + "..." + password[-1]

#Lets pretend we are Firefox (will fail otherwise)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }


regions = { 'BB': 1, 'BA': 2, 'KE': 3, 'NR': 4, 'PO': 5, 'TR': 6,
            'TT': 7, 'ZA':8, 'ABR':10,'CZ': 9 }


f = open("/home/arkonix/tmp/scrap.html","w")

def log(msg):
    print msg

def login(user_name, password):
    url = 'https://prihlasenie.azet.sk/overenie?isWap=0'

    #Login encoded url
    data = 'form%5Busername%5D=' + user_name + \
     '&form%5Bpassword%5D=' + password + '&PosliForm=PosliForm&OK=Prihlasit'

    req = urllib2.Request(url, data, headers=headers)

    log("Logging into pokec.sk")
    response = urllib2.urlopen(req)
    the_page = response.read()

    soup = bs4.BeautifulSoup(the_page)
    
    tag = soup.find(text="klikni sem")
    if tag == None:
        raise Exception("""Seems that the session could not be established. 
            Do you have the correct username and password?""")
    
    tag = tag.parent
    session_id = tag["href"].split("?i9=")[1]

    log("Success")
    
    return session_id



def count_users (args, session_id):
        url = 'http://pokec.azet.sk/sluzby/pouzivatelia/' + user_name + '/?i9=' + session_id
        
        if args[0] == 0:
            gender = 1
            gender_str = "male"
        elif args[0] == 1:
            gender = 2
            gender_str = "female"
        else:
            raise ValueError("Gender value must be either 0 or 1")
        
        region_w = None    
        for r in regions.items():
            if r[1] == args[1]:
                region_w = r[0]
                break
        
        if region_w == None:
            raise ValueError("Illegal value for the region: " + str(args[1]))
        
        region =  "k_" + str(args[1])
        
        age_from = str(args[2])
        age_to = str(args[3])
        
        
        q_args = '&nick=&filtrovat=1&pohlavie=' + str(gender) + \
         '&vekOd=' + age_from + '&vekDo=' + age_to + '&region='  \
         + region + '&vzdialenost=0&akt-miest=a_0&i9=' + session_id
        
        log("Filtering users based on criteria: gender: " + gender_str + \
            ", region: " + region_w + ", age: " + age_from + " - " + age_to)
        #log("Query arguments: " + q_args)

        req = urllib2.Request(url + q_args, headers=headers)
        response = urllib2.urlopen(req)
        
        the_page = response.read()
        
        soup = bs4.BeautifulSoup(the_page)
        
        
        def find_count_tag(tag):
            return (tag.name == "span" 
                    and tag.parent.name == "button" 
                    and re.match("Zobrazi.*\(\d*\)", unicode(tag.string), re.UNICODE))
        
        tags = soup.find_all(find_count_tag)
        
        if (len(tags) == 0):
            print the_page
            print >> f, the_page 
            raise Exception("""Could not retrieve the user count from the server response. 
            Probably bad input or number of users too big""")
        
        assert len(tags) == 1
        
        text = unicode(tags[0].string)
        count =  int(re.findall("\d+", text, re.UNICODE)[0])
        
        log("Found " + str(count) + " results")
        return count


def go():
    session_id = login(user_name, password)
    
    region = 'BA'
    min_age = 14
    max_age = 70
    age_diff = 0

    genders = {'male': 0, 'female': 1}

    for k in genders:
        gender = genders[k]

        count = 0
        for age in range(min_age, max_age + 2, 1 + age_diff): 
            params = (gender, regions[region], age, age + age_diff)
            count = count +  count_users(params, session_id)
    
        print "Total " + k  + " : " + str(count) 


go()