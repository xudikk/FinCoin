from contextlib import closing

from django.db import connection
from methodism import custom_response, dictfetchall

from base.errors import MSG
from base.helper import lang_helper
from core.models import Product
from core.models.core import Backed


def add_backed(request, params):
    if "product_id" not in params:
        return custom_response(False, message=MSG['ParamsNotFull'][lang_helper(request)])

    product = Product.objects.filter(id=params['product_id']).first()
    if not product:
        return custom_response(False, message=MSG['NotData'][lang_helper(request)])

    backed = Backed.objects.get_or_create(product=product, user=request.user)[0]
    backed.quantity = params.get('quantity', backed.quantity)
    backed.save()
    return custom_response(True, data=MSG['Success'][lang_helper(request)])


def see_backed(request):
    sql = f"""
    select bc.*, pr.name as product_name, pr.img as product_img  from core_backed bc
    inner join core_product pr on pr.id = bc.product_id 
    where bc.user_id={request.user.id}
    """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        mentors = dictfetchall(cursor)

    return custom_response(True, data=mentors)




