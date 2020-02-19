import requests         #Getting webpages
import json             #Handling 4chan's JSON output
import lxml.html as lh  #Parsing story information out of Giantessworld recent's page
import re               #For cleaning thread title/giantessworld title text (just to be safe)

#Returns a list of 4chan threads, each in the format: (title,link)
def getGTSthreads():
    r = requests.get("https://a.4cdn.org/d/catalog.json")

    #Get all threads with these keywords in the title
    keywords = ['giant','shrink','shrunk','omnipotence']

    #Output list
    sizeThreads = list()

    #If the request was successful
    if r.ok:
        #Parse it as JSON, then iterate through threads
        d = r.json()
        for page in d:
            for thread in page['threads']:
                #For every thread that has a subtitle, operate on ones that have certain keywords
                if 'sub' in thread:
                    ismatch = 0
                    for word in keywords:
                        if word in thread['sub'].lower():
                            ismatch = 1
                    if ismatch:
                        out = (re.sub(r"[^a-zA-Z0-9:\-\\'/ ]",'',thread['sub']),f'https://boards.4chan.org/d/thread/{thread["no"]}')
                        sizeThreads.append(out)

    return sizeThreads

#Returns a list of Giantessworld links in a format ready to be inserted to the sidebar. In the format "* [title](link)"
def getGiantessworldRecents():
    #Make the request
    g = requests.get("http://giantessworld.net/browse.php?type=recent")

    #Reject stories with these keywords in the title (don't want them in the sidebar ya know)
    #Will expand as needed
    blacklist = ['teen','kid','baby']

    #If the request went through alright, do the thing. Else return nothing
    if g.ok:
        #Parse all story a-tags from the page
        page = lh.fromstring(g.content)
        stories = page.xpath("//div[@class='title']/a[starts-with(@href,'viewstory.php?sid=')]")
        
        #Return list
        output = list()

        for story in stories:
            #Get story title, but with only the characters in the regex allowed (don't want any strange characters messing anything up)
            storyTitle = re.sub(r"[^a-zA-Z0-9:\-\\'/ ]",'',story.xpath("text()")[0])

            #Check for banned words
            ban = 0
            for word in blacklist:
                if word in storyTitle.lower():
                    ban = 1

            #Append sidebar string to output if not banned word
            if not ban:
                output.append((storyTitle,f'http://www.giantessworld.net/{story.xpath("@href")[0]}&index=1'))
        
        #Output only 10 most recent max
        if len(output) > 10:
            return output[:10]
        else:
            return output
    else:
        return None    

#Run the functions and print output
def main():
    gtsworld = getGiantessworldRecents()
    chan = getGTSthreads()

    print("---GTSworld most recents---")
    for s in gtsworld:
        print(s)
    print("\n---4chan size threads---")
    for t in chan:
        print(t)

main()
