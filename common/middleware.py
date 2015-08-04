class RemoteAddrMiddleware(object):
    # This middleware class was taken from the django admin honeypot
    # documentation:
    # http://django-admin-honeypot.readthedocs.org/en/latest/manual/faq.html
    def process_request(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
            request.META['REMOTE_ADDR'] = ip
