import asyncio

async def cleanChat(client, config, message, shutdownFlag):
    # Holders
    counter = 0
    msgs = []

    await client.send_message(message.channel, 'Calculating number of messages to delete...')

    async for log in client.logs_from(message.channel):
        if str(log.author.id) == client.user.id or log.content.startswith(config.Command_Prefix):
            msgs.append(log)
            counter += 1

    if len(msgs) < 2:
        await client.delete_message(msgs[0])
    elif len(msgs) <= 100:
        await client.delete_messages(msgs)

    if shutdownFlag:
        # Just a funny message
        await client.send_message(message.channel, 'I was always taught to leave a place better than I found it, {} total deleted messages.' .format(counter+1))
    else:
        await client.send_message(message.channel, 'You have deleted {} messages...  Well make that {} messages' .format(counter, counter+1))
        
    await asyncio.sleep(3)

    async for log in client.logs_from(message.channel):
        if str(log.author.id) == client.user.id:
            await client.delete_message(log)
