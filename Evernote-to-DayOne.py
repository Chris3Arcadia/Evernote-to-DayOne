#!/usr/bin/env python
# coding: utf-8

# Evernote to Day One Migration Script

# Copyright © 2021, Christopher E. Arcadia

# add libraries
import os # for file input/output
import lxml.html # for parsing HTML
import datetime # for converting timestamp to formatted data
import geopy # for converting geolocation data to location name
import pypandoc # for converting body to markdown (requires Pandoc installation)
import subprocess # for scripting through command line
import time # enable pauses for uplods
import urllib # for dealing with html encoded string

# set options
path = dict()
path['in'] = '/Users/me/Recipes_html' # input folder with HTML files
path['out'] = '/Users/me/Recipes_md' # output folder to save MD files
path['exe'] = '/usr/local/bin/dayone2' # path of sh file for the Day One Command Line Interface
form = dict()
form['in'] = 'html' # input format
form['out'] = 'txt' # output format
options = dict()
options['write'] = True # convert Evernote notes to Markdown files
options['command'] = True # write Markdown files to Day One using the Command Line Interfac
options['journal'] = 'My-Evernote-Journal' # destination Day One journal 
options['pause'] = 20 # seconds to pause between uploads
options['limit'] = 30 # maximum allowed number of photos

# locate files
if os.path.exists(path['in']):            
    directory = os.listdir(path['in'])
    files = [file[0:-(len(form['in'])+1)] for file in directory if os.path.isfile(os.path.join(path['in'], file))
            and file.split('.')[-1].lower()==form['in'] and file[0:2]!='._']    
    print('Found '+str(len(files))+' files.\n')
    for n in range(len(files)):
        print(str(n)+' : '+files[n])

# prepare output path   
if options['write']:
    if not os.path.exists(path['out']):
        os.mkdir(path['out'])
        print('Created output path.\n')

# convert all files
counter = 1
geolocator = geopy.geocoders.Nominatim(user_agent="GenericAppName")
for file in files:

    # notify
    print('Converting file #'+str(counter)+': "'+file+'"')
    
    # get file contents    
    filename = os.path.join(path['in'],file+'.'+form['in'])
    tree = lxml.html.parse(filename)

    # break the file up into parts
    header = tree.find('head')
    title = header.find('title')
    metadata = header.findall('meta')
    body = tree.find('body')
    images = [child for child in tree.iter("img")]
    references = [child for child in tree.iter("a")]

    # get all metadata
    info = dict()
    info['title'] = ''
    info['source-url'] = ''
    info['created'] = ''
    info['latitude'] = ''
    info['longitude'] = ''    
    for meta in metadata:
        attributes = meta.attrib
        if 'name' in attributes:
            info[attributes['name']] = attributes['content']   
    info['title'] = title.text_content() 

    # format fields needed for DayOne
    about = dict()
    about['Title'] = info['title']
    about['Timestamp'] = info['created']
    if info['created']:
        date = datetime.datetime.strptime(info['created'], '%Y-%m-%d %H:%M:%S %z')
        about['Date'] = date.strftime('%B %d, %Y at %I:%M:%S %p %Z')
    else:
        about['Date'] = ''    
    if info['latitude'] and info['longitude']:
        about['Coordinates'] = info['latitude']+', '+info['longitude']
        about['Location'] = geolocator.reverse(about['Coordinates']).address
    else:
        about['Location'] = ''
    about['Reference'] = info['source-url']
    
    # convert body html to markdown
    content = lxml.html.tostring(body)
    content = pypandoc.convert_text(content,'gfm',format='html-native_divs-native_spans')    
    content = content.replace('<span>','').replace('</span>','')

    # write content to new file
    if options['write']:
        filename = os.path.join(path['out'],file+'.'+form['out'])
        with open(filename, 'w') as writer:
            try:
                for key in ['Date','Location']:                
                    writer.write('\t'+key+': '+about[key]+'\n')   
                writer.write('\n')
                writer.write('# '+about['Title']+'\n')
                writer.write('\n')        
                writer.write(content)
                writer.write('\n')        
                for key in about.keys():                
                    writer.write('> **'+key+'**: '+about[key]+'\n')   
            finally:
                writer.close()    
                
    # write content to DayOne (using the official command line interface)
    if options['command']:
        bash = ['dayone2','--journal',options['journal']]
        if info['latitude'] and info['longitude']:
            bash = bash + ['--coordinate',info['latitude'],info['longitude']]
        if info['created']:
            date2 = info['created'].split()
            bash = bash + ['--isoDate=',date2[0]+'T'+date2[1]]
            bash = bash + ['-z','GMT'+date2[2]]              
        if images:
            num = len(images)            
            bash = bash + ['-photos']
            imageList = []
            imageCounter = 1
            for im in images:
                if 'src' in im.attrib and imageCounter<=options['limit']:
                    imOrig = im.attrib['src']
                    imClean = urllib.parse.unquote(imOrig)
                    bash = bash + [os.path.join(path['in'],imClean)]    
                    imageList = imageList + [imClean]
                    imageCounter = imageCounter + 1
            if num>0:
                bash = bash +['--']
            if num>options['limit']:
                print('Warning: '+about['Title']+' has over '+str(options['limit'])+' photos ('+str(num)+').')
        bash = bash + ['new','# '+about['Title']+'\n']    
        content = content.replace('![](','> (')
        bash = bash + ['\n',content,'\n']
        for key in about.keys():                
            bash = bash + ['> **'+key+'**: '+about[key]+'\n']   
        bash = bash + ['> **Attachments**:\n'] 
        if images:
            for n in range(len(imageList)):
                bash = bash + ['>`'+imageList[n]+'`\n']
        if references:
            for ref in references:
                if 'href' in ref.attrib:
                    bash = bash + ['>`'+ref.attrib['href']+'`\n']                    
        proc = subprocess.Popen(bash, executable=path['exe'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        o, e = proc.communicate()        
        flag = proc.returncode
        if flag:
            try:
                print('Error: '  + e.decode('ascii'))  
                print('Output: ' + o.decode('ascii'))
            except:
                print('Error: '  + str(e))
                print('Output: ' + str(o))
            print('Code: ' + str(flag))

    # pause to let uploads occur
    if options['pause']:
        time.sleep(options['pause'])            

    # increment counter
    counter = counter + 1