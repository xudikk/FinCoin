#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
import datetime
import uuid

from methodism import custom_response, generate_key

from base.errors import MSG
from base.helper import lang_helper, generate_number, look_at_params, make_transfer
from core.models import User, Card
from core.models.monitoring import Monitoring


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


def transfer(request, params):
    res = look_at_params(params, ['token', 'to_card', 'amount'])
    print(res)
    if res:
        return custom_response(False, message=MSG['ParamsNotFull'][lang_helper(request)])
    sender_card = Card.objects.filter(token=params['token']).first()
    reciever_card = Card.objects.filter(number=params['to_card']).first()
    if not sender_card:
        return custom_response(False, message=MSG['SenderCardNotFound'][lang_helper(request)])
    if not reciever_card:
        return custom_response(False, message=MSG['ReceiverCardNotFound'][lang_helper(request)])
    if sender_card.blocked:
        return custom_response(False, message=MSG['CantTransferUsingViaCard'][lang_helper(request)])
    if reciever_card.blocked:
        return custom_response(False, message=MSG['CantTransferUsingToCard'][lang_helper(request)])
    if sender_card == reciever_card:
        return custom_response(False, message=MSG['TransferToReceiverDenied'][lang_helper(request)])
    if request.user != sender_card.user:
        return custom_response(False, message=MSG['PermissionDenied'][lang_helper(request)])

    if sender_card.balance < int(params['amount']):
        return custom_response(False, message=MSG['BalanceInfluence'][lang_helper(request)])
    data = {
        "tr_id": generate_key(50),
        'sender': sender_card,
        'sender_token': sender_card.token,
        'receiver': reciever_card,
        'receiver_token': reciever_card.token,
        'amount': params['amount'],
    }
    monitoring = Monitoring.objects.create(**data)
    monitoring.status = 1 if make_transfer(sender_card, reciever_card, params['amount']) else 2
    monitoring.save()

    return custom_response(True, data=monitoring.response(), message=MSG['Success'][lang_helper(request)])

























