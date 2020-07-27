import os
import django
import csv
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE","config.settings")
django.setup()

from product.models import *

CSV_PATH = ['./men_가방, 지갑.csv']
CSV_PATH.append('./men_니트.csv')
CSV_PATH.append('./men_바지.csv')
CSV_PATH.append('./men_상.csv')
CSV_PATH.append('./men_셔츠.csv')
CSV_PATH.append('./men_수영복.csv')
CSV_PATH.append('./men_신발.csv')
CSV_PATH.append('./men_아우터.csv')
CSV_PATH.append('./men_아이웨어.csv')
CSV_PATH.append('./men_액세서리.csv')
CSV_PATH.append('./men_주얼리.csv')
CSV_PATH.append('./men_only.csv')
CSV_PATH.append('./women_니트.csv')
CSV_PATH.append('./women_데님.csv')
CSV_PATH.append('./women_바지.csv')
CSV_PATH.append('./women_수영복.csv')
CSV_PATH.append('./women_스포츠웨어.csv')
CSV_PATH.append('./women_아우터.csv')
CSV_PATH.append('./women_원피스.csv')
CSV_PATH.append('./women_이너웨어.csv')
CSV_PATH.append('./women_치마.csv')
CSV_PATH.append('./women_홈웨어.csv')
CSV_PATH.append('./women_up.csv')
CSV_PATH.append('./women_only.csv')

for CSV in CSV_PATH:
    with open(CSV) as in_file:
        data_reader = csv.reader(in_file)
        for row in data_reader:
            category=row[0]
            subcategory=row[1]
            detail=row[2]
            brand=row[3]
            brand_text=row[4]
            brand_logo=row[5]
            product=row[6]
            price=float(row[7].replace(",",""))
            discount_rate=row[8]
            if discount_rate != '':
                discount_rate=float(discount_rate)
            else:
                discount_rate=0
            discount_price=row[9]
            if discount_price != '':
                discount_price=float(discount_price)
            else:
                discount_price=0
            image=row[10].replace("뿌"," ").split()
            if not Category.objects.filter(name=category).exists():
                Category.objects.create(name=category)
            if not Subcategory.objects.filter(name=subcategory).exists():
                Subcategory.objects.create(name=subcategory)
            if not Detail.objects.filter(name=detail).exists():
                Detail.objects.create(name=detail)
            if not Brand.objects.filter(name=brand).exists():
                Brand.objects.create(name=brand,desc=brand_text,logo_url=brand_logo)
            if not Product.objects.filter(name=product).exists():
                Product.objects.create(name=product,price=price,discount_rate=discount_rate,discount_price=discount_price,
                brand=Brand.objects.get(name=brand),category=Category.objects.get(name=category),subcategory=Subcategory.objects.get(name=subcategory),
                detail=Detail.objects.get(name=detail),delivery_fee=0)
            for i in range(len(image)):
                if not Image.objects.filter(image=image[i]).exists():
                    Image.objects.create(image=image[i],product=Product.objects.get(name=product))
            if not BrandCategory.objects.filter(category=Category.objects.get(name=category), brand=Brand.objects.get(name=brand)).exists():
                BrandCategory.objects.create(category=Category.objects.get(name=category), brand=Brand.objects.get(name=brand))
            if not CategorySubcategory.objects.filter(category=Category.objects.get(name=category),subcategory=Subcategory.objects.get(name=subcategory)).exists():
                CategorySubcategory.objects.create(category=Category.objects.get(name=category),subcategory=Subcategory.objects.get(name=subcategory))
            de=Detail.objects.get(name=detail)
            de.category_subcategory=CategorySubcategory.objects.get(category=Category.objects.get(name=category),subcategory=Subcategory.objects.get(name=subcategory))
            de.save()

CSV='./special.csv'
with open(CSV) as in_file:
    data_reader = csv.reader(in_file)
    for row in data_reader:
        orderimage          = row[0]
        title               = row[1]
        subtitle            = row[2]
        dday                = row[3]
        background          = row[4]
        category            = row[5]
        subcategory         = row[6]
        detail=row[7]
        brand=row[8]
        brand_text=row[9]
        brand_logo=row[10]
        product=row[11]
        price=float(row[12].replace(",",""))
        discount_rate=row[13]
        if discount_rate != '':
            discount_rate=float(discount_rate)
        else:
            discount_rate=0
        discount_price=row[14]
        if discount_price != '':
            discount_price=float(discount_price)
        else:
            discount_price=0
        image=row[15].replace("뿌"," ").split()
        if not Category.objects.filter(name=category).exists():
            Category.objects.create(name=category)
        if not Subcategory.objects.filter(name=subcategory).exists():
            Subcategory.objects.create(name=subcategory)
        if not Detail.objects.filter(name=detail).exists():
            Detail.objects.create(name=detail)
        if not Brand.objects.filter(name=brand).exists():
            Brand.objects.create(name=brand,desc=brand_text,logo_url=brand_logo)
        if not Product.objects.filter(name=product).exists():
            Product.objects.create(name=product,price=price,discount_rate=discount_rate,discount_price=discount_price,
            brand=Brand.objects.get(name=brand),category=Category.objects.get(name=category),subcategory=Subcategory.objects.get(name=subcategory),
            detail=Detail.objects.get(name=detail),delivery_fee=0)
        for i in range(len(image)):
            if not Image.objects.filter(image=image[i]).exists():
                Image.objects.create(image=image[i],product=Product.objects.get(name=product))
        if not BrandCategory.objects.filter(category=Category.objects.get(name=category), brand=Brand.objects.get(name=brand)).exists():
            BrandCategory.objects.create(category=Category.objects.get(name=category), brand=Brand.objects.get(name=brand))
        if not CategorySubcategory.objects.filter(category=Category.objects.get(name=category),subcategory=Subcategory.objects.get(name=subcategory)).exists():
            CategorySubcategory.objects.create(category=Category.objects.get(name=category),subcategory=Subcategory.objects.get(name=subcategory))
        de=Detail.objects.get(name=detail)
        de.category_subcategory=CategorySubcategory.objects.get(category=Category.objects.get(name=category),subcategory=Subcategory.objects.get(name=subcategory))
        de.save()

        if not SpecialOrder.objects.filter(title=title).exists():
            SpecialOrder.objects.create(title=title,subtitle=subtitle,time=dday,product=Product.objects.get(name=product),image=orderimage,background_image=background)
        
