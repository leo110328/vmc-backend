from rest_framework.renderers import JSONRenderer


class customrenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:

            if isinstance(data, dict):
                msg = data.pop('msg', 'success')
                code = data.pop('code', renderer_context["response"].status_code)
            else:
                msg = 'success'
                code = renderer_context["response"].status_code

            # 自定义返回数据格式
            ret = {
                'code': 0,
                'msg': msg,
                'data': data,
            }
            if code == 0:
                ret.pop('data')
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)
