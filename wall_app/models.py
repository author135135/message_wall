from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey, TreeManager


class Comment(MPTTModel):
    text = models.TextField()
    parent = TreeForeignKey('self', blank=True, null=True, default=None, related_name='children')
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    tree_manager = TreeManager()

    class MPTTMeta:
        level_attr = 'mptt_level'

    class Meta:
        ordering = ('-created_at',)

    def __unicode__(self):
        return self.text

    def get_except(self, length=50):
        return u'{}'.format(self.text[:length])
    get_except.short_description = 'Comment except'

    @staticmethod
    def build_tree(comments, parent=None):
        res = []

        # Get all objects from list of ids
        if not parent:
            comments = Comment.tree_manager.filter(id__in=[t[0] for t in comments]).select_related('user')

        qs_list = [c for c in comments if c.parent_id == parent]

        if not parent:
            qs_list = reversed(qs_list)

        for comment in qs_list:
            comment_dict = {
                'comment': comment,
                'children': Comment.build_tree(comments, comment.id)
            }

            res.append(comment_dict)

        return res
