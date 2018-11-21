import django_filters
import django_tables2 as tables
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .models import *

class PlayerTable(tables.Table):
    view = tables.TemplateColumn('<a href={% url "player_view" record.id %} class="btn btn-info" role="button">View</a>', verbose_name='View')
    edit = tables.TemplateColumn('<a href={% url "player_edit" record.id %} class="btn btn-success" role="button">Edit</a>', verbose_name='Edit')
    delete = tables.TemplateColumn('<a href={% url "player_delete" record.id %} class="btn btn-danger" role="button">Delete</a>', verbose_name='Delete')
    class Meta:
        model = Player
        template_name = 'django_tables2/bootstrap4.html'
        # Change weird field names
        club_id = tables.Column(verbose_name='Club Name')
        sequence = ('first_name', 'middle_name', 'last_name')
        # Exclude stuff we don't want
        exclude= ('created_at', 'updated_at', 'id')

class PlayerFilter(django_filters.FilterSet):
    class Meta:
        model = Player
        fields = ['classification', 'grade', 'club_id']

class FilteredPlayerListView(SingleTableMixin, FilterView):
    table_class = PlayerTable
    model = Player
    template_name = 'cc_management/players/players.html'

    filterset_class = PlayerFilter