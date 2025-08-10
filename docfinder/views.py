from django.shortcuts import render
from .models import Provider

US_STATE_CHOICES = [
    ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
    ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
    ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
    ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
    ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
    ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
    ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
    ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
    ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
    ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
    ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
    ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
    ('DC', 'District of Columbia'), ('PR', 'Puerto Rico'), ('GU', 'Guam'),
    ('VI', 'U.S. Virgin Islands'), ('AS', 'American Samoa'), ('MP', 'Northern Mariana Islands')
]

def search_view(request):
    query_params = {
        'last_name': request.GET.get('last_name', ''),
        'first_name': request.GET.get('first_name', ''),
        'city': request.GET.get('city', ''),
        'state': request.GET.get('state', ''),
        'zip': request.GET.get('zip', ''),
        'description': request.GET.get('description', ''),
    }

    # Start with no results
    results = []
    show_results = False

    if any(query_params.values()):
        show_results = True
        results = Provider.objects.all()

        if query_params['last_name']:
            results = results.filter(last_name__icontains=query_params['last_name'])
        if query_params['first_name']:
            results = results.filter(first_name__icontains=query_params['first_name'])
        if query_params['city']:
            results = results.filter(city__icontains=query_params['city'])
        if query_params['state']:
            results = results.filter(state__iexact=query_params['state'])
        if query_params['zip']:
            results = results.filter(zip__icontains=query_params['zip'])
        if query_params['description']:
            results = results.filter(
                providertaxonomy__taxonomy__display_name__icontains=query_params['description']
            ).distinct()
    context = {
        'results': results,
        'query': query_params,
        'show_results': show_results,
        'state_choices': US_STATE_CHOICES,
    }
    return render(request, 'search.html', context)
