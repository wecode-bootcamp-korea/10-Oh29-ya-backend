import os, django, csv, sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from sns.models import Staff, Post, Hashtag, PostHashtag

CSV_PATH = './29tv.csv'

with open(CSV_PATH, encoding='utf-8') as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    '''
    ##########PostHashtag Table##########
    #set @cnt=0;
    #update table_name set field_name=@cnt:=@cnt+1;
    #alter table table_name auto_increment=1;
    #####################################
    for row in data_reader:
        post_id = Post.objects.get(thumbnail_img=row[0]).id
        #print(post_id)
        hashtag_list = row[5].split(' ')
        for element in hashtag_list:
            hash_id = Hashtag.objects.get(name=element).id
            PostHashtag.objects.create(hashtags_id=hash_id, posts_id=post_id)
    '''


    '''
    ##########Hashtag Table##########
    hashtag_list = []
    for row in data_reader:
        hashtag = row[5].split(' ')
        for element in hashtag:
            if element in hashtag_list:
                pass
            else:
                hashtag_list.append(element)
    for element in hashtag_list:
        Hashtag.objects.create(name=element)
    '''


    '''
    ##########Post Table##########
    for row in data_reader:
        content = row[4]
        content = content.encode('utf-8').decode('utf-8')
        thumbnail_img = row[0]
        staff_id = Staff.objects.get(name=row[2]).id
        Post.objects.create(content=content, thumbnail_img=thumbnail_img, staff_id=staff_id)
    '''


    '''
    ##########Staff Table##########
    name_list = []
    for row in data_reader:
        if row[2] in name_list:
            pass
        else:
            staff_logo = row[1]
            staff_name = row[2]
            official_check = row[3]
            name_list.append(row[2])
            Staff.objects.create(name=staff_name, logo=staff_logo, official=official_check)
    '''
