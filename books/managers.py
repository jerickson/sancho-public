from datetime import date, datetime, timedelta
from django.db import models
from django.utils.timezone import utc


class HighlightManager(models.Manager):

    def this_week(self):
        """
        QuerySet for highlighted passages collected this week.
        """
        today = date.today()
        start_week = today - timedelta(today.weekday())
        end_week = start_week + timedelta(7)
        return self.get_query_set().filter(created_at__range=[start_week, end_week])

    def random(self):
        """ Returns a random passage from any book or story. """
        return self.get_query_set().order_by('?')[0:1]

    def top_rated(self):
        """ Select the highest rated passages liked in the last month. """
        now = datetime.utcnow().replace(tzinfo=utc)
        thirty_days_ago = now - timedelta(days=160)
        qs = self.get_query_set().filter(last_liked__range=[thirty_days_ago, now])
        return qs.order_by("-likes", "-last_liked")
