#!/usr/bin/env python
# coding: utf-8

# In[162]:


import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
#from wordcloud import WordCloud
import emoji


# In[163]:


# Load the chat data into a list
#with open('WhatsApp Chat with CAPG - DOJ PENDING.txt', 'r', encoding='utf-8') as file:
    #chat = file.readlines()


# In[164]:


f = open('WhatsApp Chat with CAPG - DOJ PENDING.txt', 'r', encoding='utf-8')
chat=f.read()


# In[165]:


print(type(chat))


# In[166]:


# Define a regular expression pattern to match the date and time stamp
date_pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[AP]M\s-\s'


# In[167]:


messages = re.split(date_pattern, chat)[1:]
messages


# In[168]:


dates = re.findall(date_pattern, chat)
dates


# In[169]:


a={'user_message': messages, 'message_date': dates}
df = pd.DataFrame().from_dict(a, orient='index')
df=df.transpose()
    # convert message_date type
df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')
#df['datetime'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p')
df.rename(columns={'message_date' : 'date'}, inplace=True)
df.head()


# In[170]:


users = []
messages = []
for message in df['user_message']:
    entry = re.split('([\w\W]+?):\s', message)
    if entry[1:]:  # user name
        users.append(entry[1])
        messages.append(" ".join(entry[2:]))
    else:
        users.append('group_notification')
        messages.append(entry[0])
df['user'] = users
df['message'] = messages
df.drop(columns=['user_message'], inplace=True)
        
df.head()


# In[171]:


df.shape


# In[172]:


df['year'] = df['date'].dt.year
df.head()


# In[173]:


df['month'] = df['date'].dt.month_name()
df.head()


# In[174]:


df['day'] = df['date'].dt.day
df.head()


# In[175]:


df['hour'] = df['date'].dt.hour
df.head()


# In[176]:


df['minute'] = df['date'].dt.minute
df.head()


# In[177]:


df.head()


# In[178]:


df[df['user'] == '+91 9665835824'].shape


# In[179]:


# fetch the total number of words
words = []
for message in df['message']:
   words.extend(message.split())


# In[180]:


len(words)


# In[181]:


df[df['message'] == '<Media omitted>\n'].shape[0]


# In[182]:


from urlextract import URLExtract

extractor=URLExtract()

urls=extractor.find_urls("Let's have URL stackoverflow.com as an example google.com, http://facebook.com, ftp://url.in")
urls


# In[183]:


# fetch number of links shared
links = []
for message in df['message']:
    links.extend(extractor.find_urls(message))


# In[184]:


len(links)


# In[185]:


df


# In[186]:


x=df['user'].value_counts().head()


# In[187]:


import matplotlib.pyplot as plt


# In[188]:


name = x.index
count = x.values


# In[189]:


plt.bar(name,count)
plt.xticks(rotation='vertical')
plt.show()


# In[190]:


temp=df[df['user'] !='group_notification']
temp=temp[temp['message'] !='<Media omitted>\n']


# In[191]:


f= open('english1.txt','r')
stop_words = f.read()
print(stop_words)


# In[192]:


words = []

for message in temp['message']:
    for word in message.lower().split():
        if word not in stop_words:
            words.append(word)


# In[193]:


from collections import Counter
pd.DataFrame(Counter(words).most_common(20))


# In[194]:


import emoji


# In[195]:


emojis = []
for message in df['message']:
    emojis.extend([c for c in message])


# In[196]:


pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))


# In[197]:


emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))


# In[198]:


plt.bar(emoji_df[0].head(),emoji_df[1].head())


# In[199]:


df['month_num'] = df['date'].dt.month


# In[200]:


df


# In[201]:


timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()


# In[202]:


timeline


# In[203]:


time = []
for i in range(timeline.shape[0]):
    time.append(timeline['month'][i] +"-" +str(timeline['year'][i]))


# In[204]:


timeline['time'] = time


# In[205]:


timeline


# In[206]:


plt.plot(timeline['time'],timeline['message'])
plt.xticks(rotation='vertical')
plt.show()


# In[207]:


df['only_date'] = df['date'].dt.date


# In[208]:


daily_timeline = df.groupby('only_date').count()['message'].reset_index()


# In[209]:


plt.figure(figsize=(18,10))
plt.plot(daily_timeline['only_date'],daily_timeline['message'])


# In[210]:


df['day_name'] = df['date'].dt.day_name()


# In[211]:


df['day_name'].value_counts()


# In[212]:


df['month'] = df['date'].dt.day_name()


# In[213]:


df['month'].value_counts()


# In[214]:


df.head()


# In[215]:


period = []
for hour in df[['day_name', 'hour']]['hour']:
    if hour == 23:
        period.append(str(hour)+ "-" + str('00'))
    elif hour == 0:
        period.append(str('00')+ "-" + str(hour+1))
    else:
        period.append(str(hour)+ "-" + str(hour+1))
            


# In[216]:


df['period'] = period


# In[217]:


df.sample(5)


# In[218]:


import seaborn as sns
plt.figure(figsize=(20,6))
sns.heatmap(df.pivot_table(index='day_name' ,columns='period' ,values='message',aggfunc='count').fillna(0))
plt.yticks(rotation='horizontal')
plt.show()


# In[219]:


df.pivot_table(index='day_name' ,columns='period' ,values='message',aggfunc='count').fillna(0)


# In[252]:





# In[3]:


# Split the chat data into messages using the date and time stamp as delimiter
messages = []

for line in chat:
    if re.match(date_pattern, line):
        messages.append(line.strip())
    else:
        messages[-1] += ' ' + line.strip()
# Split the messages into date, time, author, and message
parsed_messages = []
for message in messages:
    match = re.match(r'(\d{1,2}/\d{1,2}/\d{2}),\s(\d{1,2}:\d{2}\s[AP]M)\s-\s([^:]+):\s(.*)', message)
    if match:
        parsed_messages.append({
            'date': match.group(1),
            'time': match.group(2),
            'author': match.group(3),
            'message': match.group(4)
        })


# In[ ]:





# In[253]:


# Convert the parsed messages into a pandas DataFrame
df = pd.DataFrame(parsed_messages)


# In[254]:


# Convert the parsed messages into a pandas DataFrame
df = pd.DataFrame(parsed_messages)


# In[255]:


# Convert the date and time columns to datetime objects
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%m/%d/%y %I:%M %p')


# In[256]:





# In[257]:


# Extract the hour of the day from the datetime column
df['hour'] = df['datetime'].dt.hour
df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month_name()
df['day'] = df['datetime'].dt.day


# In[242]:


# Extract the day of the week from the datetime column
df['weekday'] = df['datetime'].dt.weekday


# In[243]:


df.head()


# In[244]:


df.shape


# In[245]:


# Fetch unique users
unique_users = df['author'].unique()


# In[246]:


# Stats Area
total_messages = len(df)
total_users = len(unique_users)
messages_per_user = total_messages / total_users
avg_message_length = df['message'].str.len().mean()

print("Total Messages: ", total_messages)
print("Total Users: ", total_users)
print("Messages per User: ", messages_per_user)
print("Average Message Length: ", avg_message_length)


# In[247]:


# Monthly timeline
monthly_timeline = df.groupby(pd.Grouper(key='datetime', freq='M'))['message'].count().reset_index()
plt.figure(figsize=(16, 6))
sns.lineplot(x='datetime', y='message', data=monthly_timeline)
plt.title('Monthly Timeline')
plt.xlabel('Month')
plt.ylabel('Number of Messages')
plt.show()


# In[248]:


# Daily timeline
daily_timeline = df.groupby(pd.Grouper(key='datetime', freq='D'))['message'].count().reset_index()
plt.figure(figsize=(16, 6))
sns.lineplot(x='datetime', y='message', data=daily_timeline)
plt.title('Daily Timeline')
plt.xlabel('Day')
plt.ylabel('Number of Messages')
plt.show()


# In[249]:


# Activity map
activity_map = df.pivot_table(index='hour', columns='weekday', values='message', aggfunc='count')
plt.figure(figsize=(12, 6))
sns.heatmap(activity_map, cmap='cool', annot=True, fmt='.2f')
plt.title('Activity Map')
plt.xlabel('Weekday')
plt.ylabel('Hour')
plt.show()


# In[250]:


print(unique_users)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




