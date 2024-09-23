import re
import pandas as pd
def preprocess(data):
    pattern = r'\[\d{1,2}/\d{1,2}/\d{1,2}, \d{1,2}:\d{1,2}:\d{1,2}\u202f[AP]M\]'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = df['message_date'].str.extract(r'\[(.*?)\]')[0]
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M:%S %p')
    df['message_date'] = df['message_date'].dt.strftime('%d/%m/%y, %I:%M:%S %p')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    # Loop through each message in the 'user_message' column
    for message in df['user_message']:
        # Split based on the pattern of 'username: message'
        entry = re.split(r'([^:]+):\s', message, maxsplit=1)

        if len(entry) > 2:  # If the split was successful
            users.append(entry[1].strip())  # Add the username to the users list
            messages.append(entry[2].strip())  # Add the message to the messages list
        else:
            users.append('group_notification')  # Default value for notifications
            messages.append(entry[0].strip())  # Add the whole message as it is

    # Add the extracted data back to the DataFrame
    df['user'] = users
    df['message'] = messages

    # Drop the original 'user_message' column
    df.drop(columns=['user_message'], inplace=True)

    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M:%S %p')
    df['only_date']= df['date'].dt.date
    df['day_name']=df['date'].dt.day_name()
    df['year'] = df['date'].dt.year
    df['month_num']=df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['am_pm'] = df['date'].dt.strftime('%p')



    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
           period.append("11 PM - 12 AM")
        elif hour == 0:
            period.append("12 AM - 1 AM")
        elif hour < 12:
             period.append(f"{hour} AM - {hour + 1} AM")
        elif hour == 12:
             period.append("12 PM - 1 PM")
        elif hour < 23:
             period.append(f"{hour - 12} PM - {hour - 11} PM")

# Return the DataFrame with the new period column if you're adding it to the DataFrame.
    df['period'] = period
    return df
    
    
                        


    return df
