from django.views.generic import TemplateView, RedirectView, CreateView
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import get_template
from wall_app.models import Comment
from wall_app.forms import CommentForm


class HomeView(CreateView):
    template_name = 'wall_app/home.html'
    success_url = reverse_lazy('wall_app:home')
    form_class = CommentForm
    objects_per_page = 5

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            response_data = {}

            if request.GET.get('edit') or request.GET.get('to_comment'):
                context = self._get_additional_context()

                rendered_content = get_template('wall_app/template_parts/wrap_comment_form.html').render(context)

                response_data = {
                    'content': rendered_content,
                }
            elif request.GET.get('page'):
                paginator = Paginator(Comment.objects.filter(parent=None), self.objects_per_page)
                page_obj = paginator.page(self.request.GET.get('page'))

                qs = Comment.tree_manager.get_queryset_descendants(
                    Comment.tree_manager.filter(id__in=page_obj.object_list),
                    include_self=True)

                rendered_content = get_template('wall_app/template_parts/comments.html').render({
                    'comments': Comment.build_tree(qs.values_list('id')),
                    'request': self.request,
                })

                response_data['content'] = rendered_content
                response_data['has_next'] = page_obj.has_next()

            return JsonResponse(response_data)
        return super(HomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        paginator = Paginator(Comment.objects.filter(parent=None), self.objects_per_page)
        page_obj = paginator.page(self.request.GET.get('page', 1))

        qs = Comment.tree_manager.get_queryset_descendants(Comment.tree_manager.filter(id__in=page_obj.object_list),
                                                           include_self=True)

        context['comments'] = Comment.build_tree(qs.values_list('id'))
        context['page_obj'] = page_obj

        context.update(self._get_additional_context())

        return context

    def _get_additional_context(self):
        context = {}

        # validate data if requested some action (edit, comment, etc...)
        to_comment = self.request.GET.get('to_comment', None)
        edit = self.request.GET.get('edit', None)

        context['action'] = {}

        if to_comment or edit:
            # Check if comment exists
            try:
                comment_id = int(to_comment or edit)
                comment = Comment.objects.get(id=comment_id)

                if comment:
                    # handle requested action
                    initial_data = self.get_initial()

                    initial_data['type'] = 'additional'

                    if edit:
                        # Check if user is owner of comment
                        assert self.request.user.is_superuser or (comment.user == self.request.user)

                        initial_data['text'] = comment.text
                        initial_data['pk'] = comment.id
                        context['action']['action_type'] = 'edit'
                    elif to_comment:
                        initial_data['parent'] = comment.id
                        context['action']['action_type'] = 'to_comment'

                    # Check form type, if additional form submit re-init main form for prevent duplicate errors
                    if self.request.POST.get('type') == 'additional':
                        form = self.form_class(self.request.POST or None, initial=initial_data)
                        context['form'] = self.form_class(initial={'user': self.request.user})
                    else:
                        form = self.form_class(initial=initial_data)

                    context['action'].update({
                        'comment_id': comment.id,
                        'form': form,
                    })

            except (TypeError, Comment.DoesNotExist, AssertionError):
                pass

        return context

    def get_initial(self):
        return {
            'user': self.request.user
        }

    def form_valid(self, form):
        response = super(HomeView, self).form_valid(form)

        if self.request.is_ajax():
            response_data = {}

            rendered_content = get_template('wall_app/template_parts/comments.html').render({
                'comments': [{'comment': form.instance}],
                'request': self.request,
            })

            response_data = {
                'content': rendered_content,
            }

            return JsonResponse(response_data)
        return response

    def form_invalid(self, form):
        response = super(HomeView, self).form_invalid(form)

        if self.request.is_ajax():
            response_data = {}

            response_data = {
                'errors': form.errors,
            }

            return JsonResponse(response_data)
        return response


home = HomeView.as_view()


class AccountLoginView(TemplateView):
    template_name = 'wall_app/account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('wall_app:home'))
        return super(AccountLoginView, self).dispatch(request, *args, **kwargs)


account_login = AccountLoginView.as_view()


class AccountLogoutView(RedirectView):
    url = reverse_lazy('wall_app:home')
    permanent = False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return HttpResponseRedirect(reverse('wall_app:home'))
        return super(AccountLogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(self.request)

        return super(AccountLogoutView, self).get(request, *args, **kwargs)


account_logout = AccountLogoutView.as_view()
