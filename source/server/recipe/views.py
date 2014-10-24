from django.core import serializers
from django.http import HttpResponse
from common.models import Recipe
from common.models import Ingredient
from common.models import User

def _list(request):
    recipes = Recipe.objects.all()
    data = serializers.serialize("json", recipes)
    response_kwargs = dict()
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)


def detail(request, id):
    recipe = Recipe.objects.get(id=id)
    data = serializers.serialize("json", [recipe])
    response_kwargs = dict()
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)

def search(request):

    """
        version1
        search: using ingredient name and gastronomist name
        form: http://127.0.0.1:8000/recipe/searchrecipe?gastronomistname=linan&ingredientname=1

        version2
        search: using ingredient name(maybe more than one) and gastronomist name
        form: http://127.0.0.1:8000/recipe/searchrecipe?gastronomistname=linan&ingredientname=1,2,3
        and gastronomistname and igredientname may be none
        form: http://127.0.0.1:8000/recipe/searchrecipe?gastronomistname=&ingredientname=1,2,3
    """

    recipes = Recipe.objects.all()
    ingrname = request.GET.get('ingredientname')
    if ingrname !='':
        ingredientnamelist  = ingrname.split(',')
        for ingredientname in ingredientnamelist:
            ingredient = Ingredient.objects.get(name=ingredientname)
            ingredientid = ingredient.id
            recipes = recipes.filter(ingredients=ingredientid)

    gastronomistname = request.GET.get('gastronomistname')
    if gastronomistname != '':
        gastronomist = User.objects.get(username=gastronomistname)
        gastronomistid = gastronomist.id
        recipes = recipes.filter(gastronomist=gastronomistid)

    data = serializers.serialize("json", recipes)
    response_kwargs = dict()
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)
