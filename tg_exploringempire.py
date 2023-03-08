import asyncio
import codecs
import datetime
from telethon import TelegramClient, events

# Replace the values below with your own
api_id = 23143262
api_hash = '85660ba7289a891e292f7ea4e838276f'
phone_number = '+15206661289'

# Initialize the client with your API credentials
client = TelegramClient('session_name', api_id, api_hash)

# Define the event handler for the .chatid command
@client.on(events.NewMessage(pattern=r'/chatid'))
async def handler(event):
    # Get the chat ID of the group
    chat_id = event.chat_id
    
    # Write the chat ID to the group.txt file
    with open('group.txt', 'a') as f:
        f.write(str(chat_id) + '\n')
    # Print the chat ID to the console
    print(f'Chat ID: {chat_id}')

    # Send a message with the chat ID
    await client.send_message(event.chat_id, f'{chat_id}\n')

async def main():
    # Start the client
    await client.start(phone_number)

    # Define the list of group IDs to send the message to
    group_ids = []
    with open('group.txt', 'r') as f:
        group_ids = [int(line.strip()) for line in f.readlines()]

    # Read the message from the file
    with codecs.open('post.txt', 'r', encoding='utf-8') as f:
        message = f.read().encode('unicode_escape').decode('unicode_escape')

    # Set the initial timer value
    last_sent_time = datetime.datetime.now()

    while True:
        # Send the message to each group
        for group_id in group_ids:
            await client.send_message(group_id, message)
            current_time = datetime.datetime.now()
            time_since_last_send = current_time - last_sent_time
            time_remaining = datetime.timedelta(seconds=20) - time_since_last_send
            while time_remaining.total_seconds() > 0:
                print(f'Message sent successfully to group ID {group_id}. Next message in {time_remaining.total_seconds():.0f} seconds.', end='\r')
                await asyncio.sleep(1)
                current_time = datetime.datetime.now()
                time_since_last_send = current_time - last_sent_time
                time_remaining = datetime.timedelta(seconds=20) - time_since_last_send
                
            last_sent_time = current_time
            print('\n')   
        # Wait for 60 seconds before sending the message again
        await asyncio.sleep(10)
    # Keep the client running to receive updates
    await client.run_until_disconnected()

asyncio.run(main())
