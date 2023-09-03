#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan


MSG = {
    # user
    "UserAlreadyDeleted": {
        "uz": "Foydalanuvchi allaqachon o'chirib yuborilgan",
        "ru": "Пользователь уже удален",
        "en": "User Already Deleted",
    },
    "PasswordError": {
        'uz': "Noto'g'ri parol",
        'ru': "Неверный пароль",
        'en': "Incorrect password",
    },
    "LoggedOut": {
        'uz': "User sistemadan chiqarildi",
        'ru': "Пользователь вышел из системы",
        'en': "User has been logged out",
    },
    "SuccessLangChanged": {
        "uz": "Til O'zgartirildi",
        "ru": "Язык изменён",
        "en": "language changed",
    },
    "PasswordChanged": {
        'uz': "Parol muaffaqiyatli o'zgartirildi",
        'ru': "Пароль успешно изменен",
        'en': "Password changed successfully",
    },
    "SenderCardNotFound": {
        "uz": "Yuboruvchi kartasi topilmadi",
        "ru": "Карта отправителя не найдена",
        "en": "Sender card not found"
    },
    "SenderTokenRequired": {
        'uz': "Yuboruvchi tokeni bo'lishi shart",
        "ru": "Должен быть токен отправителя",
        "en": "Must have sender token"
    },
    "ErrorSenderToken": {
        'uz': "Yuboruvchi tokeni xato",
        "en": "Sender token is invalid",
        "ru": "Должен быть токен отправителя"
    },
    "NotUniredCard": {
        "uz": "Ushbu karta Unired visa kartasi emas",
        "ru": "Эта карта не является картой Unired Visa.",
        "en": "This card is not a Unired visa card"
    },
    "CardError": {
        'uz': "Kartalarda xatolik",
        'ru': "Проблема с картой",
        'en': "Error with cards"
    },
    "CardSuccessDeleted": {
        'uz': "Karta muvoffaqiyatli o'chirib tashlandi",
        "ru": "Карта успешно удалена",
        'en': "Card deleted successfully"
    },
    "UserDeleted": {
        'uz': f"Ushbu user active emas yoki o'chirib yuborilgan",
        'ru': f"Этот пользователь был удален",
        'en': f"This user has been deleted",
    },
    "UserSuccessDeleted": {
        'uz': "User muvoffaqiyatli o'chirib tashlandi",
        "ru": "User успешно удалена",
        'en': "User deleted successfully"
    },
    "PhoneAndCardPhoneError": {
        "uz": "Telefon raqami tog'ri kelmaganligi sababli siz ushbu raqamni qo'sha olmaysiz",
        "ru": "Вы не можете добавить этот номер, потому что телефон не подходит",
        'en': "You cannot add this number because the phone does not match"
    },

    # auth
    'UUIDBlocked': {
        'uz': "Ushbu UUID Blocklangan",
        'ru': "Этот UUID заблокирован",
        'en': "This UUID is blocked",
    },
    'UUIDNotOrBlocked': {
        'uz': "Ushbu UUID Topilmadi yoki Blocklangan",
        'ru': "Этот UUID Не найден или заблокирован",
        'en': "This UUID is Not Found or Blocked",
    },
    'UUIDExpired': {
        'uz': "Ushbu UUID Eskirgan",
        'ru': "Этот UUID устарел",
        'en': "This UUID is expired",
    },
    "NotAuthenticated": {
        'uz': "Autorizatsiya Talab qilinadi!",
        'ru': 'Требуется Авторизация!',
        'en': "Authorization Required!"
    },
    "ErrorOTP": {
        'uz': "OTP xatoligi",
        'ru': 'Проблема с ОТП',
        'en': "OTP Error"
    },
    "UUIDError": {
        'uz': "UUID xatoligi",
        'ru': 'Проблема с UUID',
        'en': "UUID Error"
    },
    "OTPExpired": {
        'uz': "OTP token eskirgan",
        'ru': "Токен OTP устарел",
        'en': "OTP token is expired",
    },
    'OTPTokenError': {
        "uz": "Otp token xato",
        "ru": "Ошибка токена OTP",
        "en": "Otp token error"
    },
    "UserExist": {
        'uz': "Bu telefon raqam orqali allaqachon ro'yxatdan o'tilgan",
        'ru': "Этот номер телефона уже зарегистрирован",
        'en': "This phone number is already registered",
    },
    "LENPHONE": {
        'uz': "Telefon raqam uzunligi 12ta bo'lishi kerak",
        'ru': "Длина номера телефона должен быть 12 символ",
        'en': "Phone number length must be 12 characters",
    },
    "Unauthenticated": {
        'uz': "Ro'yhatdan o'tmagan",
        'ru': 'Неаутентифицированный',
        'en': "Unauthenticated",
    },
    "TokenUnUsable": {
        'uz': "Yaroqsiz Token",
        'ru': "Просроченный Токен",
        'en': "Expired Token",
    },
    "AuthToken": {
        'uz': "Token aniqlanmadi",
        'ru': "Token не найден",
        'en': "Token not fount",
    },
    'OTPPhoneAndPhoneNotMatch': {
        "uz": "OTP bilan telefon raqam tog'ri kelmadi",
        "ru": "Номер телефона не совпал с OTP",
        "en": "The phone number did not match with OTP"
    },
    'OtpError': {
        "uz": "Maxfiy code xato",
        "en": "Wrong  secret code",
        "ru": "Неправильный секретный код",
    },

    # Data Errors
    'ParamsNotFull': {
        "uz": "< params > to'lliq emas",
        "ru": "< params> неполные",
        "en": "< params > is incomplete"
    },
    "ParamsMustList": {
        "uz": "< params > list(array) ko'rinishida bo'lishi kerak",
        "ru": "<params> должен быть в виде списка(array)",
        "en": "< params > must be in list(array) form"
    },
    "ParamsMust": {
        "uz": "< params > bo'lishi shart",
        "ru": "< params > Должен быть",
        "en": "< params > must be filled"
    },
    "MethodMust": {
        "uz": "Method bo'lishi shart",
        "ru": "Должен быть метод",
        "en": "Method must be filled"
    },
    "DataNotFull": {
        'uz': "Kerakli ma'lumotlar kiritilmagan",
        'en': "Required information not entered",
        "ru": "Не введена необходимая информация"
    },
    "ErrorData": {
        "uz": 'Xato ma\'lumot',
        "ru": 'Неправильные данные',
        "en": 'Incorrect data',
    },
    # "PasswordMust": {
    #     'uz': f"< password > to'ldirishili shart",
    #     'ru': f"< password > to'ldirishili shart",
    #     'en': f"< password > должен быть заполнен",
    # },
    "ErrorMethod": {
        "uz": "Method xato",
        "ru": "Неправильный Method",
        "en": "Invalid Method",
    },
    "TokenMust": {
        'uz': f"Token to'ldirishili shart",
        'ru': f"Токен должен быть заполнен",
        'en': f"Token must be filled",
    },
    "ReceiverOrToken": {
        "uz": f"< params.receiver_token > yoki < params.receiver > bo'lishi shart",
        "ru": f"Должен быть < params.receiver_token > или < params.receiver >",
        "en": f"< params.receiver_token > or < params.receiver > must be filled"
    },
    "CardNumberInvalid": {
        "uz": f"< card_number > tog'ri emas",
        "ru": f"Номер карты неверный < card_number >",
        "en": f"< card_number > not valid"
    },


    # Permision Errors
    "CardCantTransfer": {
        'uz': "Bunday karta orqali o'tqazma qilishni imkoni yo'q",
        'ru': "Депозит через такую карту невозможен",
        'en': "It is not possible to make a deposit through such a card",
    },
    "CantTransferUsingViaCard": {
        'uz': "Ushbu karta orqali o'tkazma qilib bo'lmaydi",
        "ru": "Переводы с этой карты невозможны",
        'en': "Transfers cannot be made using this card",
    },
    "TransferToReceiverDenied": {
        'uz': "Ushbu kartaga o'tkazma qilib bo'lmaydi",
        "ru": "Переводы с для карты невозможны",
        'en': "Transfers cannot be made to this card"
    },
    'DeviceRevokeDenited': {
        "uz": "Ushbu qurulma boshqalarini chiqarib yubora olmaydi",
        "ru": "Это устройство не может отозвать другое",
        "en": "This device can't revoke another one",
    },
    # "BlockSessionDenied": {
    #     'uz': "Bu qurilma boshqasini bekor qila olmaydi",
    #     'ru': "Это устройство не может отозвать другое",
    #     'en': "This device can't revoke another one",
    # },
    # "BlockPrimaryDenied": {
    #     'uz': "Bu qurilmani bekor qila olmaysiz",
    #     'ru': "Вы не можете отозвать это устройство",
    #     'en': "You can't revoke this device",
    # },
    'PermissionDenied': {
        'uz': "Sizda bu amalni bajarish uchun ruxsat yo‘q",
        'ru': 'У вас нет разрешения на выполнение этого действия',
        'en': "You do not have permission to perform this action",
    },
    'UserRevokeDenited': {
        "uz": "Siz bu qurulmani o'chirib yubora olmaysiz",
        "ru": "Вы не можете отозвать это устройство",
        "en": "You can't revoke this device",
    },
    "AlreadyBlocked": {
        "uz": "Ushbu qurulma allaqachon blocklangan",
        "ru": "Это устройство уже заблокировано",
        "en": "This device already blocked",
    },


    # Not Fount Errors
    "ServiceDoesNotExist": {
        "uz": "Hozircha Bunday xizmat mavjud emas",
        "ru": "Эта услуга в настоящее время недоступна",
        "en": "This service is currently unavailable"
    },
    "ReceiverCardNotFound": {
        'uz': "Receiver Karta topilmadi",
        "ru": "Receiver Карта не найдена",
        'en': "Receiver Card not found"
    },
    "NotInformationCard": {
        "uz": "Hech qanday karta ma'lumoti yo'q",
        "ru": "Нет информации о карте",
        'en': 'No card information'
    },
    "SessionNotFound": {
        'uz': "Ushbu qurulma topilmadi",
        'ru': "Это устройство не найдено",
        'en': "This device is not found",
    },
    'CardNotFound': {
        'uz': "Karta topilmadi",
        "ru": "Карта не найдена",
        'en': "Card not found"
    },
    "UserNotFound": {
        'uz': "Foydalanuvchi topilmadi",
        'ru': "Пользователь не найден",
        'en': "User Not Found",
    },
    "NewNotFound": {
        "uz": "Bunday yangilik topilmadi",
        "ru": "Таких новостей не найдено",
        "en": "No such news was found",
    },
    'MethodDoesNotExist': {
        'uz': f"Bunday method topilmadi",
        'ru': f"Такой метод не найден",
        'en': f"No such method found",
    },
    "NotData": {
        'uz': "Ma'lumot topilmadi",
        "ru": "Информация не найдена",
        "en": "No information found"
    },
    "NotDataTrID": {
        "uz": "Ushbu tr_id bo'yicha ma'lumot topilmadi",
        "ru": "Информация для этого tr_id не найдена",
        "en": "No information found for this tr_id"
    },
    "CantFindReceiverCard": {
        "uz": "Qabul qiluvchi kartasi tokenini aniqlab bo'lmadi",
        "ru": "Токен карты получателя не может быть идентифицирован",
        "en": "The receiver card token could not be identified"
    },


    # Other Errors
    "InvalidBasicHeader1": {
        'uz': "Basic headerda xatolik | Maʼlumotlar taqdim etilmaydi",
        'ru': "Неверный базовый заголовок | Учетные данные не предоставлены",
        'en': "Invalid basic header | No credentials provided",
    },
    "InvalidBasicHeader2": {
        'uz': "Basic headerda xatolik | Hisob maʼlumotlari qatorida boʻsh joy boʻlmasligi kerak.",
        'ru': "Неверный базовый заголовок | Строка учетных данных не должна содержать пробелов.",
        'en': "Invalid basic header | Credentials string should not contain spaces.",
    },
    "InvalidBasicHeader3": {
        'uz': "Basic headerda xatolik | Maʼlumotlar base64 da to'g'ri kodlanmagan",
        'ru': "Неверный базовый заголовок | Учетные данные неправильно закодированы в base64",
        'en': "Invalid basic header | Credentials not correctly base64 encoded",
    },
    'UndefinedError': {
        "uz": "Nomalum xatolik yuz berdi",
        "ru": "Произошла неопределенная ошибка",
        "en": "Undefined error occurred",
    },
    "Success": {
        'uz': "Muaffaqiyatli",
        'ru': 'Успешно',
        'en': "Success"
    },
}
