'use strict'
$ ->

    csrftoken = Cookies.get('csrftoken')
    csrfSafeMethod = (method) ->
        # these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));

    $.ajaxSetup({
        beforeSend: (xhr, settings) ->
            if (!csrfSafeMethod(settings.type) && !this.crossDomain)
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
    });

    window.clone_object = (obj) ->
        if not obj? or typeof obj isnt 'object'
            return obj

        if obj instanceof Date
            return new Date(obj.getTime()) 

        if obj instanceof RegExp
            flags = ''
            flags += 'g' if obj.global?
            flags += 'i' if obj.ignoreCase?
            flags += 'm' if obj.multiline?
            flags += 'y' if obj.sticky?
            return new RegExp(obj.source, flags) 

        newInstance = new obj.constructor()

        for key of obj
            newInstance[key] = clone_object obj[key]

        return newInstance
