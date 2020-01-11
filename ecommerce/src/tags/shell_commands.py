# python manage.py shell

from tags.models import Tag

qs = Tag.objects.all()
qs 
# <QuerySet [<Tag: T shirt>, <Tag: Tshirt>, <Tag: T-shirt>, <Tag: Red>, <Tag: Black>]>

black = Tag.objects.last()
black.title 
# 'Black'

printblack.slug 
#'black'

black.active
# True

black.products
 # <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager at 0x10393f1d0>

black.products.all()
# <ProductQuerySet [<Product: Hat>, <Product: T-shirt>]>

black.products.all().first()
# <Product: Hat>

exit()


# python manage.py shell
from products.models import Product

qs = Product.objects.all()

qs
# <ProductQuerySet [<Product: Hat>, <Product: T-shirt>, <Product: Computer>, <Product: Long desc>]>

tshirt = qs.first()
tshirt
# <Product: Hat>

tshirt.title
# 'Hat'

tshirt.desc
# 'This is an awesome hat. Buy it!'

tshirt.tag_set
# <django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager at 0x112b72358>

tshirt.tag_set.all()
# <QuerySet [<Tag: Red>, <Tag: Black>]>

tshirt.tag_set.filter(title__iexact="Black")
# <QuerySet [<Tag: Black>]>

exit()