SMS_ERROR = 1000
VCODE_ERROR = 1001
LOGIN_REQUIRED = 1002
PROFILE_ERROR = 1003
EXCEED_MAXIMUM_REWIND = 1004
NO_RECORD = 1005


class LogicError(Exception):
    code = None
    data = None


# 定义一个生成异常类的工厂方法
def gen_logic_err(name, code, data):
    return type(name, (LogicError,), {'code': code, 'data': data})


SmsError = gen_logic_err('Sms_Error', code=1000, data='短信发送失败')
VcodeError = gen_logic_err('Vcode_Error', code=1001, data='短信验证码错误')
LoginRequired = gen_logic_err('Login_Required', code=1002, data='请登录')
ProfileError = gen_logic_err('Profile_Error', code=1003, data='个人交友资料数据不合法')
ExceedMaximumRewind = gen_logic_err('Exceed_Maximum_Rewind', code=1004, data='超过最大反悔次数')
NoRecord = gen_logic_err('No_Record', code=1005, data='没有记录，无法反悔')

