#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from methodism.helper import custom_response as cr

from core.v1.services.auth import login, auth_two, resent_otp, add_bonus_to_all
from core.v1.services.user import set_lang, check_pass, change_pass, user_edit
from core.v1.services.monitoring import all_card, create_card, transfer
from core.v1.services.shop import see_backed, add_backed

""" Method Names Getter """

unusable_method = dir()


def method_names(requests):
    return cr(True, data=[x.replace('_', '.') for x in unusable_method if '__' not in x and x != 'cr'])

