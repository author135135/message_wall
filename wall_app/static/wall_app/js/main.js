(function($){
    $(document).ready(function(){
        $(document).on('submit', 'form', function(e){
            e.preventDefault();

            var form = $(this),
                reply_or_edit = form.parent().hasClass('well');

            $('.has-error', form).removeClass('has_error');
            $('.help-block', form).remove();


            // Check csrftoken
            if (!$('[name="csrfmiddlewaretoken"]', form).length) {
                form.append('<input type="hidden" name="csrfmiddlewaretoken" value="' + getCookie('csrftoken') + '">');
            }

            $.post(form.attr('action'), form.serialize(), function(response){
                if (response['errors']) {
                    $.each(response['errors'], function(k, v){
                        $('[name="' + k + '"]', form).parents('.form-group').addClass('has-error');
                        $('[name="' + k + '"]', form).after('<span class="help-block">' + v + '</span>');
                    });
                } else {
                    if (reply_or_edit) {
                        // Check reply or edit form
                        var entity_pk = $('[name="pk"]', form).val();

                        form = form.parents('.well');

                        if (entity_pk) {
                            // Edit
                            var content = $.parseHTML(response['content']);

                            $('.media-body', content).append($('~ .media', form).clone());

                            form.parent().parent().replaceWith(content);
                        } else {
                            // Reply
                            $('> .label', form.prev()).removeClass('disabled');

                            if ($('~ .media', form).length) {
                                $('~ .media:last', form).after(response['content']);
                                form.remove();
                            } else {
                                form.replaceWith(response['content']);
                            }
                        }
                    } else {
                        form.after(response['content']);
                        form.trigger('reset');
                    }
                }
            }, 'json');
        });

        $(document).on('click', '.media .label', function(e){
            e.preventDefault();

            var link = $(this),
                link_wrap = link.parent();

            if (link.hasClass('disabled')) {
                return false;
            }

            if ($('+ .well', link_wrap).length) {
                $('+ .well', link.parent()).remove();
            }

            $.get(link.attr('href'), {}, function(response){
                link_wrap.after(response['content']);

                $('+ .well h4', link_wrap).append('<a class="close">&times;</a>');

                $('> .label', link_wrap).addClass('disabled');
            }, 'json');
        });

        $(document).on('click', '.well h4 .close', function(e) {
            var form_wrap = $(this).parents('.well');

            $('> .label', form_wrap.prev()).removeClass('disabled');

            form_wrap.remove();
        });

        // Rebuild default paginator as Load More button
        if ($('.pager').length) {
            var next_page_link = $('.pager li:last-child a'),
                pager_html = '';

            pager_html += '<div class="pager-wrap col-sm-4 col-sm-offset-4">';
            pager_html += '<a class="btn btn-block btn-default has-spinner" href="' + next_page_link.attr('href') + '">';
            pager_html += '<span class="spinner"><i class="glyphicon glyphicon-refresh gly-spin"></i></span>Load more</a>';
            pager_html += '</div>';

            $('.pager').replaceWith(pager_html);

            $('.pager-wrap a').click(function(e) {
                e.preventDefault();

                if ($(this).hasClass('active')) {
                    return false;
                }

                var link = $(this),
                    url_info = new Url(link.attr('href'));

                link.addClass('active');

                $.get(link.attr('href'), {}, function(response) {
                     $('.pager-wrap').before(response['content']);

                    if (response['has_next']) {
                        url_info.query['page'] = parseInt(url_info.query['page']) + 1;

                        link.attr('href', url_info);
                        link.removeClass('active');
                    } else {
                        $('.pager-wrap').remove();
                    }
                }, 'json');
            });
        }

        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    });
})(jQuery);