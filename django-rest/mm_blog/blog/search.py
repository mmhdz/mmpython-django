from rest_framework.filters import SearchFilter
from .models import BlogPost



class SearchFiltterMutipleValues(SearchFilter):
    
    def filter_queryset(self, request, queryset, view):
        search_terms = request.query_params.get(self.search_param, '').split(",")
        if len(search_terms) > 1:
            return BlogPost.objects.filter(hashtags__value__in=search_terms)
        
        return super().filter_queryset(request, queryset, view)