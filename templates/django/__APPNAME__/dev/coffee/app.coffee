'use strict'
$ ->

    window.myparseInt = (value) ->
        val = parseInt(value.replace(/[\.,]/g, ''))
        return val or 0

    window.reinitWidgets = (base) ->
        $(base + ' .select2:not(.select2-container), ' + base + ' .select2-nosearch').each ->
            options = {}
            if $(this).hasClass('select2-nosearch')
                options['minimumResultsForSearch'] = Infinity
            if $(this).hasClass('select2-format')
                for ffuncname in ['templateResult', 'templateSelection', 'escapeMarkup']
                    ffunc = $(this).data(ffuncname.toLowerCase())
                    if ffunc
                        options[ffuncname] = eval(ffunc)
            $(this).select2(options)
            true
        $(base + ' .toggle-chkbox').bootstrapSwitch()
        $(base + ' .switch-radio2').bootstrapSwitch()
        $(base + ' [data-toggle="popover"]').popover()
        # $(base + ' .date-field').datepicker
        #     showISOWeekNumbers: true,
        #     autoApply: true,
        #     autoclose: true,
        #     todayBtn: 'linked',
        #     # container: '.seldatediv',
        #     todayHighlight: true,
        #     minViewMode: 'days',
        #     maxViewMode: 'years',
        #     format: 'mm/dd/yyyy',
        #     opens: "right"
        true

    window.pass = () ->
        # does nothing, just a stub
        return false

    $(document).on 'click', '.post-button,.delete-button,.ajax-form-submit-button', () ->
        # simple POST/DELETE
        confirm_msg = $(this).data('confirm')
        if confirm_msg
            if not confirm(confirm_msg)
                return false
        sendmethod = 'POST'
        if $(this).hasClass('delete-button')
            sendmethod = 'DELETE'
        posturl = $(this).data('url') or '?'
        pparr = posturl.split('?')
        posturl = pparr[0]
        params = pparr[1]
        if $(this).hasClass('ajax-form-submit-button')
            params = {}
            form = $(this).closest('form')
            $('.form-control', form).each ->
                fname = $(this).attr('name')
                type = $(this).attr('type')
                fvalue = $(this).val()
                if type == 'checkbox'
                    fvalue = $(this).data("bootstrap-switch").state()
                params[fname] = fvalue
                true
            formaction = $(form).attr('action')
            # if formaction != null and formaction != ''
            posturl = formaction || posturl
            sendmethod = $(form).attr('method') || sendmethod
        $.ajax posturl,
            type: sendmethod,
            data: params,
            # dataType: 'json',
            success: (data, textStatus, jqXHR) ->
                if data == 'OK'
                    true
                else
                    if data[0..8] == 'redirect:'
                        newurl = data[9..1000]
                        if newurl == '-'
                            newurl = window.location
                        window.location = newurl
                    else
                        alert(data)
            error: (jqXHR, textStatus, error) ->
                console.log(jqXHR)
                console.log(textStatus)
                console.log(error)
        if $(this).data('no-propagate')
            return false
        true

    $(document).on 'click', '.openmodal-button', () ->
        target = $(this).data('modal-target')
        if target
            $(target).modal('show')
        else
            url = $(this).data('modal-url')
            $.ajax url,
                type: 'GET'
                dataType: 'html'
                success: (data, textStatus, jqXHR) ->
                    $(".modal-element").html(data)
                    $(".modal-element .modal").modal('show')
                error: (jqXHR, textStatus, error) ->
                    console.log(jqXHR)
                    console.log(textStatus)
                    console.log(error)
        return false

    $(document).on "click", ".not-implemented", (e) ->
        e.preventDefault()
        alert("This feature is not implemented yet")
        false

    $(document).on "click", "a.disabled", (e) ->
        e.preventDefault()
        false

    reinitWidgets('body')
