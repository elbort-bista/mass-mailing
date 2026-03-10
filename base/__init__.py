from django.template.context import Context, RequestContext

def context_copy(self):
    c = self.__class__()
    c.dicts = self.dicts[:]
    c.autoescape = self.autoescape
    return c

def request_context_copy(self):
    c = Context()
    c.dicts = self.dicts[:]
    c.autoescape = self.autoescape
    c.request = self.request
    return c

Context.__copy__ = context_copy
RequestContext.__copy__ = request_context_copy
