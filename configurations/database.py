# coding: utf-8
import pymongo
import sys
import time

client = pymongo.MongoClient(
    "mongodb+srv://ashvini1991:qD3R%g4#d2@koib-wz4jx.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('koi')
job_send_record = db.job_notification
result_sent_record = db.result_announcement
admit_card_record = db.admit_card


"""
job_send_record.remove({})
result_sent_record.remove({})
admit_card_record.remove({})


sys.exit("Error message")
"""


"""
lt =job_send_record.find(
    {'$and': [
        {'chat_id': 321641669},
        {'url': {'$in': [
            'http://www.freejobalert.com/rsmssb-patwari/820875/',
            'https://www.tcckerala.com/uploads/ckeditor_files/1592302063_website+notification+workers+2020.pdf',
            'google.jli'

        ]}}
    ]}
)
"""


"""
username_available = job_send_record.aggregate(
    [
        {"$group": {"_id": {'chat_id': "$chat_id",'name':"$name", 'username': "$username", 'first_name': "$first_name"}}}
    ]
)


for x in username_available:
	print('\n',x['_id']['chat_id'])
	print( x )


sys.exit("stop message")
"""