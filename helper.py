from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
from transformers import pipeline
import emoji 
extract=URLExtract()
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)
def fetch_stats(selected_user,df):
    if selected_user!='Overall':
       df=df[df['user']== selected_user]
       #fetch number of messages
    num_messages=df.shape[0]
       #fetch number of words
    words= []
    for message in df['message']:
        words.extend(message.split())
   #fetch number of media messages
    # Check if the 'message' column contains any of the specified media strings
    #ran code inside previuos for loop-error,format of text in doc does not contain \n
    num_media_messages = df[df['message'].str.contains(r'(video omitted|image omitted|GIF omitted|audio omitted)', na=False)].shape[0]
   #fetch number of links shared
    links = []
    for message in df['message']:
        #links.append(extract.find_urls(message))
        links.extend(extract.find_urls(message))
        

    return num_messages,len(words),num_media_messages,len(links)   
def most_busy_users(df):
    x=df['user'].value_counts().head() 
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'count':'percent','user':'name'}) 

    
    return x,df
def create_wordcloud(selected_user,df): #inaccurate
    f= open('stop_hinglish.txt','r')
    stop_words= f.read()



    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    temp=df[df['user']!='🪵WoOd🪵']
    #temp=temp[temp['message']!=r'(video omitted|image omitted|GIF omitted|audio omitted)']
    temp = temp[~temp['message'].str.contains(r'(video omitted|sticker omitted|image omitted|GIF omitted|audio omitted|omitted)', regex=True)]
    def remove_stop_words(message):
         y=[]
         
         for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
            return " ".join(y)    




        

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc
def most_common_words(selected_user,df):
    
    f= open('stop_hinglish.txt','r')
    stop_words= f.read()



    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    temp=df[df['user']!='🪵WoOd🪵']
    #temp=temp[temp['message']!=r'(video omitted|image omitted|GIF omitted|audio omitted)']
    temp = temp[~temp['message'].str.contains(r'(video omitted|sticker omitted|image omitted|GIF omitted|audio omitted|omitted)', regex=True)]
    
    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
               words.append(word)

     

    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    most_common_df.rename(columns={0: 'word', 1: 'count'}, inplace=True)


    
   
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    
    return emoji_df
def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df=df[df['user']== selected_user]

    timeline= df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']= time
    return timeline
def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']== selected_user]
    daily_timeline= df.groupby('only_date').count()['message'].reset_index() 

    return daily_timeline  
 
def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['user']== selected_user]
    return df['day_name'].value_counts()
def monthly_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']=='selected_user']

    return df['month'].value_counts()
def activity_heatmap(selected_user,df):

    if selected_user!= 'Overall':
        df=df[df['user']=='selected_user']
    user_heatmap=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return user_heatmap




    
def sentiment_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Combine all the messages from the selected user into one string
    all_messages = " ".join(df['message'].tolist())
    word_list = all_messages.split()  # Split the combined string into a list of words

    # Take the first 2000 words
    combined_message = " ".join(word_list[:200])
    print(combined_message)
    # Perform emotion analysis on the combined message
    result = emotion_model(combined_message)

    # Extract the emotion with the highest confidence
    # Sort the emotions by score in descending order
    top_emotion = sorted(result[0], key=lambda x: x['score'], reverse=True)

    # Extract the labels of the top emotions
    top_emotion_labels = [emotion['label'] for emotion in top_emotion[:5]]

    # Return the combined message and the top 5 detected emotion labels
    return top_emotion_labels






   


       
     