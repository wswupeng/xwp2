import web
import model

render = web.template.render('templates/')
admin_render = web.template.render('templates/admin', base='base')

t_globals = {
    'datestr': web.datestr,
    'model' : model,
    'render': render,
    'admin_render': admin_render
    }

web.template.Template.globals = t_globals
