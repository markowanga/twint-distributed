from client.task_client import ScrapInterval, TwintDistributedTaskClient

HASHTAGS = [
    '#wyboryprezydenckie2020',
    '#wybory2020',
    '#kidawa2020',
    '#duda2020',
    '#wypadzpałacu',
    '#bosak2020',
    '#andrzejduda2020',
    '#biedron2020',
    '#wyboryprezydenckie',
    '#prezydent2020',
    '#kosiniak2020',
    '#biedroń2020',
    '#hołownia2020',
    '#10maja2020',
    '#holownia2020',
    '#kosiniakkamysz2020',
    '#szymonhołownia2020',
    '#trzaskowski2020'
]

client = TwintDistributedTaskClient('http://192.168.0.124:5000')
for hashtag in HASHTAGS:
    print(hashtag)
    client.add_search_to_scrap(hashtag, ScrapInterval.MONTH, 'bot_detection', 'hashtag_political', since=None,
                               until=None, language='pl')
