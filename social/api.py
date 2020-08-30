from lib.http import render_json
from social import logic


def get_recd_list(request):
    """获取推荐列表"""
    user = request.user
    data = logic.get_recd_list(user)
    return render_json(data=data)


