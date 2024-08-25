# # middleware.py
from django.utils.deprecation import MiddlewareMixin
from .models import UserAgentIP

class SaveUserAgentIPMiddleware(MiddlewareMixin):
    def process_request(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        browser = request.META.get('HTTP_USER_AGENT', '')
        movie=request.COOKIES.get("movie",False)
        crawlers=request.user_agent.is_bot
        phone=request.user_agent.is_mobile
        tablet=request.user_agent.is_tablet
        pc=request.user_agent.is_pc
    # touch_capable=request.user_agent.is_touch_capable

        if crawlers:
            device='crawlers'
        elif phone:
            device='phone'
        elif tablet:
            device='tablet'
        else:
            device='pc'

        deviceOs=request.user_agent.os
    
        user_agent_ip = UserAgentIP.objects.filter(ip=ip, browser=browser).first()
   
        if user_agent_ip:
            user_agent_ip.count += 1
            user_agent_ip.movie=movie
            user_agent_ip.save()
        else:
            user_agent_ip=UserAgentIP(browser=browser,device=device,deviceOs=deviceOs,ip=ip,crawlers=crawlers,movie=movie,count=1)
            user_agent_ip.save()
        return None

# def saveUserAgentData(request):
    # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    # if x_forwarded_for:
    #     ip = x_forwarded_for.split(',')[0]
    # else:
    #     ip = request.META.get('REMOTE_ADDR')
    # browser = request.META.get('HTTP_USER_AGENT', '')
    # movie=request.COOKIES.get("movie",False)
    # crawlers=request.user_agent.is_bot
    # phone=request.user_agent.is_mobile
    # tablet=request.user_agent.is_tablet
    # pc=request.user_agent.is_pc
    # # touch_capable=request.user_agent.is_touch_capable

    # if crawlers:
    #     device='crawlers'
    # elif phone:
    #     device='phone'
    # elif tablet:
    #     device='tablet'
    # else:
    #     device='pc'

    # deviceOs=request.user_agent.os
    
    # user_agent_ip = UserAgentIP.objects.filter(ip=ip, browser=browser).first()
   
    # if user_agent_ip:
    #     user_agent_ip.count += 1
    #     user_agent_ip.movie=movie
    #     user_agent_ip.save()
    # else:
    #      user_agent_ip=UserAgentIP(browser=browser,device=device,deviceOs=deviceOs,ip=ip,crawlers=crawlers,movie=movie,count=1)
    #      user_agent_ip.save()
    # return None