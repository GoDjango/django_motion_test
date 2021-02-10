from geopy.distance import geodesic

from django.http import HttpResponse
from django.template import loader

from .models import Restaurant


# Дельта для поиска по координатам
# 0.1 - Это радиус примерно ~4-8км
DELTA = 0.1


def get_context():
    context = {'title': 'Result'}
    burger_kings = Restaurant.objects.filter(name='Burger King')
    other_restaurants = Restaurant.objects.exclude(name='Burger King')
    restaurants = []

    for bk in burger_kings:
        restaurant = {'id': bk.id,
                      'name': bk.name,
                      'address': bk.address,
                      'latitude': bk.latitude,
                      'longitude': bk.longitude,
                      }
        competitors = other_restaurants.filter(latitude__range=(bk.latitude - DELTA, bk.latitude + DELTA),
                                               longitude__range=(bk.longitude - DELTA, bk.longitude + DELTA),
                                               )

        competitors_count = 0
        competitors_kfc_count = 0
        competitors_md_count = 0
        for competitor in competitors:
            if geodesic((bk.latitude, bk.longitude), (competitor.latitude, competitor.longitude)).meters <= 2000:
                competitors_count += 1
                if competitor.name == 'KFC':
                    competitors_kfc_count += 1
                elif competitor.name == 'McDonald’s':
                    competitors_md_count += 1
        restaurant['competitors'] = competitors_count
        restaurant['competitors_kfc'] = competitors_kfc_count
        restaurant['competitors_md'] = competitors_md_count
        restaurants.append(restaurant)

    context['restaurants'] = restaurants

    return context


def index(request):
    template = loader.get_template('restaurants.html')
    context = get_context()
    return HttpResponse(template.render(context))
