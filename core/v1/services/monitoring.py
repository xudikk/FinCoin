#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
import datetime
import uuid

from methodism import custom_response

from base.errors import MSG
from base.helper import lang_helper, generate_number
from core.models import User, Card


def create_card(request, params):
    if request.user.ut not in [1, 2]:
        return custom_response(False, message=MSG['PermissionDenied'][lang_helper(request)])

    if "user_id" not in params:
        return custom_response(False, message=MSG['ParamsNotFull'][lang_helper(request)])
    user = User.objects.filter(id=params['user_id']).first()
    if not user:
        return custom_response(False, message=MSG['UserNotFound'][lang_helper(request)])

    now = datetime.datetime.now()
    card = Card.objects.create(
        user=user,
        name="Fintech Coin Card",
        balance=10_000,
        number=generate_number(),
        token=uuid.uuid4(),
        expire=f"{now.month}/{f'{now.year + 1}'[2:]}",
        is_primary=False,
        card_registered_phone=user.phone
    )
    return custom_response(True, data=card.response())


def all_card(request, params):
    cards = Card.objects.filter(user=request.user)
    return custom_response(True, data=[
        x.response() for x in cards
    ])
