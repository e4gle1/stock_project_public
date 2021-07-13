from discord_webhook import *
MOMENTUMCHANNEL = '####'
HIGHVOLMOMENTUMCHANNEL = '#####'
TECHNICALCHANNEL = '####'

def webhookDiscord(ticker):
    webhook = DiscordWebhook(url=MOMENTUMCHANNEL)
    embed = DiscordEmbed(title='MOMENTUM',
                         description=
                         f' **{ticker}**' + '\n',
                         color='0060b8')
    webhook.add_embed(embed)
    response = webhook.execute()


def webhookDiscordHV(ticker, last, stop_loss, profit, volume):
    webhook = DiscordWebhook(url=HIGHVOLMOMENTUMCHANNEL)
    embed = DiscordEmbed(title='MOMENTUM',
                         description=':mega:' +
                         f' **{ticker}**' + '\n' +
                         ':white_large_square:' + f' **${last}**' + '\n' + ':green_square:' +
                         f' **${profit}**' + '\n' +
                         ':red_square:' + f' **${stop_loss}**' + '\n' + ':yellow_square:' + f' **{volume}**',
                         color='d61a1a')
    webhook.add_embed(embed)
    response = webhook.execute()

def webhookDiscordTechnical(ticker, type, last, volume):
    webhook = DiscordWebhook(url=TECHNICALCHANNEL)
    embed = DiscordEmbed(title=f'{type}',
                         description=':mega:' +
                         f' **{ticker}**' + '\n' +
                         ':white_large_square:' + f' **${last}**'  
                          + '\n' + ':yellow_square:' + f' **{volume}**',
                         color='52aa3e')
    webhook.add_embed(embed)
    response = webhook.execute()